import pandas as pd
import re
from pandas.core.series import Series

class Trade():
    OPTION_SYMBOL_EXPRESSION = re.compile("^([A-Z]+)([0-9]{6})([PC])([0-9]{8})$")
    
    def __init__(self, trade: Series):
        self._symbol = trade.symbol
        self._parts = None

    def parts(self, partno):
        if self._parts is None:
            self._parts = self.OPTION_SYMBOL_EXPRESSION.match(self._symbol)
        return self._parts[partno]

    # Example: SPX220916C04000000    
    def symbol(self):
        return self.parts(0)
    
    # "SPX"
    def underlying(self):
        return self.parts(1)

    # "220916"
    def expirationYYMMDD(self):
        return self.parts(2)
    
    # "C" - to indicate a call contract
    # "P" - to indicate a put contract
    def contract(self):
        return self.parts(3)
    
    def isCall(self):
        return self.contract() == "C"
    
    def isPut(self):
        return self.contract() == "P"
    
    def strike(self):
        return self.parts(4)


class BoxSpreadFinder():
    def __init__(self):
        self.nearby_trades = []
        self.boxes = []
    
    def search(self, trades_df):
        trades_df = trades_df.sort_values(by=['timestamp'])
        for _, subject_trade in trades_df.iterrows():
            self._removeOutOfRangeNearbyTrades(subject_trade)
            leg_idxs = self._findBoxLegs(subject_trade)
            if leg_idxs is None:
                self.nearby_trades.append(subject_trade)
            else:
                self._addBox([subject_trade, *map(lambda idx: self.nearby_trades[idx], leg_idxs)])
                self._removeNearbyTrades(leg_idxs)

        return self._createBoxesDataframe()
    
    def _removeOutOfRangeNearbyTrades(self, subject_trade):
        max_distance = 1000
        for idx, trade in enumerate(self.nearby_trades):
            if subject_trade.timestamp - trade.timestamp < max_distance:
                self.nearby_trades = self.nearby_trades[idx:]
                return
        self.nearby_trades = []

    def _findBoxLegs(self, subject_trade):
        subject_trade_t = Trade(subject_trade)
        opposing_subject_trade_idx = None
        opposing_straddle_idxs = None
        potential_straddles = {}
        for idx, trade in enumerate(self.nearby_trades):
            trade_t = Trade(trade)
            
            # skip irrelevant trades
            if subject_trade_t.expirationYYMMDD() != trade_t.expirationYYMMDD():
                continue
            if subject_trade.volume != trade.volume:
                continue
            if subject_trade_t.strike() == trade_t.strike() and subject_trade_t.contract() == trade_t.contract():
                continue

            # look for the opposing contract
            if subject_trade_t.strike() == trade_t.strike() and subject_trade_t.contract() != trade_t.contract():
                opposing_subject_trade_idx = idx
                continue

            # find the second straddle to complete the box
            potential_straddles[f"{trade_t.contract()}{trade_t.strike()}"] = idx
            opposing_straddle_leg = f"{'P' if trade_t.isCall() else 'C'}{trade_t.strike()}"
            if opposing_straddle_leg in potential_straddles:
                opposing_straddle_idxs = (idx, potential_straddles[opposing_straddle_leg])
        
        # Check if we have a box
        if opposing_subject_trade_idx is not None and opposing_straddle_idxs is not None:
            return (opposing_subject_trade_idx, opposing_straddle_idxs[0], opposing_straddle_idxs[1])

    def _removeNearbyTrades(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.nearby_trades.pop(idx)
            
    def _addBox(self, trades):
        if len(trades) != 4:
            raise Exception("Adding a box without 4 legs")
        trades = sorted(trades, key=lambda t: t.id)
        self.boxes.append({
            'leg_1': trades[0].id,
            'leg_2': trades[1].id,
            'leg_3': trades[2].id,
            'leg_4': trades[3].id,
        })
        
    def _createBoxesDataframe(self):
        return pd.DataFrame(self.boxes)


def model(dbt, session):
    # DataFrame representing an upstream model
    trades_df = dbt.ref("trades").fetchdf()
    bsf = BoxSpreadFinder()
    return bsf.search(trades_df)

def test():
    expected_boxes = [
        {
            'leg_1': 13253,
            'leg_2': 13527,
            'leg_3': 13666,
            'leg_4': 14128
        },
        {
            'leg_1': 11052,
            'leg_2': 13528,
            'leg_3': 13667,
            'leg_4': 14129
        },
    ]
    trades = [
        { 'id': 14128, 'day': "2024-09-20", 'symbol': "SPX250620P05825000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 272.27, 'volume': 25 },
        { 'id': 13252, 'day': "2024-09-19", 'symbol': "SPX250620C05850000", 'time': "2024-09-19T17:03:25", 'timestamp': 1726766136000, 'price': 290.91, 'volume': 25 },
        { 'id': 12152, 'day': "2024-09-19", 'symbol': "SPX250620C05850000", 'time': "2024-09-19T17:03:25", 'timestamp': 1726766136000, 'price': 290.91, 'volume': 50 },
        { 'id': 13253, 'day': "2024-09-20", 'symbol': "SPX250620C05850000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 280.99, 'volume': 25 },
        { 'id': 13527, 'day': "2024-09-20", 'symbol': "SPX250620P05850000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 281.27, 'volume': 25 },
        { 'id': 13666, 'day': "2024-09-20", 'symbol': "SPX250620C05825000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 296.05, 'volume': 25 },
        { 'id': 13254, 'day': "2024-09-20", 'symbol': "SPX250620C05850000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 282.97, 'volume': 25 },
        { 'id': 13528, 'day': "2024-09-20", 'symbol': "SPX250620P05850000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 283.27, 'volume': 25 },
        { 'id': 13667, 'day': "2024-09-20", 'symbol': "SPX250620C05825000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 294.05, 'volume': 25 },
        { 'id': 11052, 'day': "2024-09-20", 'symbol': "SPX250620C05850000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 280.91, 'volume': 25 },
        { 'id': 14129, 'day': "2024-09-20", 'symbol': "SPX250620P05825000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 275.27, 'volume': 25 },
        { 'id': 10308, 'day': "2024-09-20", 'symbol': "SPX250321C05775000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 245.19, 'volume': 25 },
        { 'id': 10337, 'day': "2024-09-20", 'symbol': "SPX250321P05775000", 'time': "2024-09-20T19:04:26", 'timestamp': 1726859066910, 'price': 212.26, 'volume': 25 },
    ]
    trades_df = pd.DataFrame(trades)
    expected_boxes_df = pd.DataFrame(expected_boxes)
    bsf = BoxSpreadFinder()
    boxes = bsf.search(trades_df)
    if not boxes.equals(expected_boxes_df):
        print("expected_boxes\n", expected_boxes_df)
        print("boxes\n", boxes)
        assert False

if __name__ == '__main__':
    test()

