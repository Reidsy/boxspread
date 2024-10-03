WITH symbol_parts as (
    SELECT
        symbol
        , regexp_matches(symbol, '^([A-Z]+)([0-9]{6})([PC])([0-9]{8})$') as parts
    FROM {{ ref('symbols') }}
    GROUP BY symbol
)

, final as (
    SELECT
        symbol
        , parts[1] as underlying
        , parts[2] as expiration
        , parts[3] as put_call
        , parts[4] as strike
    FROM symbol_parts
)

SELECT * FROM final
