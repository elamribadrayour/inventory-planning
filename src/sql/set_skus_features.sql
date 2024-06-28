WITH current_data AS (
    SELECT
        sku,
        TIMESTAMP '{current_date_str}' AS dt_submitted,
        EXTRACT(DAY FROM TIMESTAMP '{current_date_str}') AS day,
        EXTRACT(YEAR FROM TIMESTAMP '{current_date_str}') AS year,
        EXTRACT(MONTH FROM TIMESTAMP '{current_date_str}') AS month,
        EXTRACT(DOW FROM TIMESTAMP '{current_date_str}') AS day_of_week,
        EXTRACT(DOY FROM TIMESTAMP '{current_date_str}') AS day_of_year,
        EXTRACT(WEEK FROM TIMESTAMP '{current_date_str}') AS week_of_year,
        CASE
            WHEN EXTRACT(DOW FROM TIMESTAMP '{current_date_str}') >= 5 THEN TRUE
            ELSE FALSE
        END AS is_weekend
    FROM (SELECT DISTINCT sku FROM features WHERE sku IN ({skus_str}))
),
lagged_features AS (
    SELECT
        sku,
        quantity_sold AS quantity_sold_lag_1,
        LAG(quantity_sold, 6) OVER (PARTITION BY sku ORDER BY dt_submitted DESC) AS quantity_sold_lag_7,
        AVG(quantity_sold) OVER (
            PARTITION BY sku
            ORDER BY dt_submitted DESC
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_mean_7,
        ROW_NUMBER() OVER (PARTITION BY sku ORDER BY dt_submitted DESC) AS rn
    FROM features
    WHERE sku IN ({skus_str})
)
SELECT
    current_data.sku,
    current_data.dt_submitted,
    current_data.day,
    current_data.year,
    current_data.month,
    current_data.day_of_week,
    current_data.day_of_year,
    current_data.week_of_year,
    current_data.is_weekend,
    COALESCE(lagged_features.quantity_sold_lag_1, 0) AS quantity_sold_lag_1,
    COALESCE(lagged_features.quantity_sold_lag_7, 0) AS quantity_sold_lag_7,
    COALESCE(lagged_features.rolling_mean_7, 0) AS rolling_mean_7
FROM current_data
LEFT JOIN lagged_features
ON current_data.sku = lagged_features.sku
WHERE lagged_features.rn = 1
