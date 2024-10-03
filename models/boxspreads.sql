WITH trades AS (
    SELECT * FROM {{ ref('trades') }}
)

SELECT
    13252 as leg_1
    , 13527 as leg_2
    , 13666 as leg_3
    , 14128 as leg_4
UNION ALL
SELECT
    13254 as leg_1
    , 13528 as leg_2
    , 13667 as leg_3
    , 14129 as leg_4
