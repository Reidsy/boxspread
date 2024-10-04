WITH symbol_parts as (
    SELECT
        symbol
        , regexp_extract(symbol, '^([A-Z]+)([0-9]{6})([PC])([0-9]{8})$', ['underlying', 'expiration', 'put_call', 'strike']) as parts
    FROM {{ ref('symbols') }}
    GROUP BY symbol
)

, final as (
    SELECT
        symbol
        , parts['underlying'] as underlying
        , parts['expiration'] as expiration
        , parts['put_call'] as put_call
        , parts['strike'] as strike
    FROM symbol_parts
)

SELECT * FROM final
