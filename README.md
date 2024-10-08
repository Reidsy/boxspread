# Boxspread

## Set up

```
poetry install
docker-compose up -d
dbt build
```

## Definition of a box spread
- must contain 4 trades
- volumes must be the same
- all trades must occur at the same time
	- ideally all trades must occur within 1 second of each other, but that query is harder
- a trade can only be part of one box spread
- The four trades must be like the following
	- Call at strike A
	- Put at strike A
	- Call at strike B
	- Put at strike B

### Example
**Query**
```
SELECT *
FROM trades
LEFT JOIN unique_symbols ON unique_symbols.symbol=trades.symbol
WHERE timestamp=1726859066910
ORDER BY volume, trades.symbol
```

**Results**
| id | day | symbol | time | timetamp | price | volume | symbol | underlying | expiration | Call/Put | Strike |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10628 | 2024-09-20 | SPX241220C05750000 | 2024-09-20T19:04:26 | 1726859066910 | 163.1 | 1 | SPX241220C05750000 | SPX | 241220 | C | 05750000 |
| 10988 | 2024-09-20 | SPX241220P05750000 | 2024-09-20T19:04:26 | 1726859066910 | 154.1 | 1 | SPX241220P05750000 | SPX | 241220 | P | 05750000 |
| 10308 | 2024-09-20 | SPX250321C05775000 | 2024-09-20T19:04:26 | 1726859066910 | 245.19 | 25 | SPX250321C05775000 | SPX | 250321 | C | 05775000 |
| 10337 | 2024-09-20 | SPX250321P05775000 | 2024-09-20T19:04:26 | 1726859066910 | 212.26 | 25 | SPX250321P05775000 | SPX | 250321 | P | 05775000 |
| 13666 | 2024-09-20 | SPX250620C05825000 | 2024-09-20T19:04:26 | 1726859066910 | 296.05 | 25 | SPX250620C05825000 | SPX | 250620 | C | 05825000 |
| 13252 | 2024-09-20 | SPX250620C05850000 | 2024-09-20T19:04:26 | 1726859066910 | 280.91 | 25 | SPX250620C05850000 | SPX | 250620 | C | 05850000 |
| 14128 | 2024-09-20 | SPX250620P05825000 | 2024-09-20T19:04:26 | 1726859066910 | 272.27 | 25 | SPX250620P05825000 | SPX | 250620 | P | 05825000 |
| 13527 | 2024-09-20 | SPX250620P05850000 | 2024-09-20T19:04:26 | 1726859066910 | 281.27 | 25 | SPX250620P05850000 | SPX | 250620 | P | 05850000 |
| 17311 | 2024-09-20 | SPX250919C05875000 | 2024-09-20T19:04:26 | 1726859066910 | 341.35 | 25 | SPX250919C05875000 | SPX | 250919 | C | 05875000 |
| 17443 | 2024-09-20 | SPX250919P05875000 | 2024-09-20T19:04:26 | 1726859066910 | 330.85 | 25 | SPX250919P05875000 | SPX | 250919 | P | 05875000 |
| 13667 | 2024-09-20 | SPX250620C05825000 | 2024-09-20T19:04:26 | 1726859066910 | 296.05 | 50 | SPX250620C05825000 | SPX | 250620 | C | 05825000 |
| 13253 | 2024-09-20 | SPX250620C05850000 | 2024-09-20T19:04:26 | 1726859066910 | 280.91 | 50 | SPX250620C05850000 | SPX | 250620 | C | 05850000 |
| 14129 | 2024-09-20 | SPX250620P05825000 | 2024-09-20T19:04:26 | 1726859066910 | 272.27 | 50 | SPX250620P05825000 | SPX | 250620 | P | 05825000 |
| 13528 | 2024-09-20 | SPX250620P05850000 | 2024-09-20T19:04:26 | 1726859066910 | 281.27 | 50 | SPX250620P05850000 | SPX | 250620 | P | 05850000 |

**Contains two box spreads**
| id | day | symbol | time | timetamp | price | volume | symbol | underlying | expiration | Call/Put | Strike |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 13667 | 2024-09-20 | SPX250620C05825000 | 2024-09-20T19:04:26 | 1726859066910 | 296.05 | 50 | SPX250620C05825000 | SPX | 250620 | C | 05825000 |
| 13253 | 2024-09-20 | SPX250620C05850000 | 2024-09-20T19:04:26 | 1726859066910 | 280.91 | 50 | SPX250620C05850000 | SPX | 250620 | C | 05850000 |
| 14129 | 2024-09-20 | SPX250620P05825000 | 2024-09-20T19:04:26 | 1726859066910 | 272.27 | 50 | SPX250620P05825000 | SPX | 250620 | P | 05825000 |
| 13528 | 2024-09-20 | SPX250620P05850000 | 2024-09-20T19:04:26 | 1726859066910 | 281.27 | 50 | SPX250620P05850000 | SPX | 250620 | P | 05850000 |


| id | day | symbol | time | timetamp | price | volume | symbol | underlying | expiration | Call/Put | Strike |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 13666 | 2024-09-20 | SPX250620C05825000 | 2024-09-20T19:04:26 | 1726859066910 | 296.05 | 25 | SPX250620C05825000 | SPX | 250620 | C | 05825000 |
| 13252 | 2024-09-20 | SPX250620C05850000 | 2024-09-20T19:04:26 | 1726859066910 | 280.91 | 25 | SPX250620C05850000 | SPX | 250620 | C | 05850000 |
| 14128 | 2024-09-20 | SPX250620P05825000 | 2024-09-20T19:04:26 | 1726859066910 | 272.27 | 25 | SPX250620P05825000 | SPX | 250620 | P | 05825000 |
| 13527 | 2024-09-20 | SPX250620P05850000 | 2024-09-20T19:04:26 | 1726859066910 | 281.27 | 25 | SPX250620P05850000 | SPX | 250620 | P | 05850000 |

**Not a box spread - only two legs (this is a straddle)**
| id | day | symbol | time | timetamp | price | volume | symbol | underlying | expiration | Call/Put | Strike |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10628 | 2024-09-20 | SPX241220C05750000 | 2024-09-20T19:04:26 | 1726859066910 | 163.1 | 1 | SPX241220C05750000 | SPX | 241220 | C | 05750000 |
| 10988 | 2024-09-20 | SPX241220P05750000 | 2024-09-20T19:04:26 | 1726859066910 | 154.1 | 1 | SPX241220P05750000 | SPX | 241220 | P | 05750000 |



**Not a box spread - different expiration dates, two separate straddles**
| id | day | symbol | time | timetamp | price | volume | symbol | underlying | expiration | Call/Put | Strike |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17311 | 2024-09-20 | SPX250919C05875000 | 2024-09-20T19:04:26 | 1726859066910 | 341.35 | 25 | SPX250919C05875000 | SPX | 250919 | C | 05875000 |
| 17443 | 2024-09-20 | SPX250919P05875000 | 2024-09-20T19:04:26 | 1726859066910 | 330.85 | 25 | SPX250919P05875000 | SPX | 250919 | P | 05875000 |
| 10308 | 2024-09-20 | SPX250321C05775000 | 2024-09-20T19:04:26 | 1726859066910 | 245.19 | 25 | SPX250321C05775000 | SPX | 250321 | C | 05775000 |
| 10337 | 2024-09-20 | SPX250321P05775000 | 2024-09-20T19:04:26 | 1726859066910 | 212.26 | 25 | SPX250321P05775000 | SPX | 250321 | P | 05775000 |




## Useful queries
```
-- bunch of trades, not a box spread
SELECT *
FROM trades
LEFT JOIN unique_symbols ON unique_symbols.symbol=trades.symbol
WHERE timestamp=1726846276591
```

```
--two box spreads, three random spreads/straddles
SELECT *
FROM trades
LEFT JOIN unique_symbols ON unique_symbols.symbol=trades.symbol
WHERE timestamp=1726859066910
ORDER BY trades.volume, unique_symbols.expiration, unique_symbols.strike, unique_symbols.put_call
```

```
-- potential boxspreads (at least 4 trades in 1 tick)
SELECT
	trades.timestamp,
	trades.volume,
	unique_symbols.expiration,
	count(*) as cnt
FROM trades
LEFT JOIN unique_symbols ON unique_symbols.symbol=trades.symbol
--WHERE timestamp = 1726859066910
GROUP BY trades.timestamp, trades.volume, unique_symbols.expiration
HAVING count(*) >=4
```
