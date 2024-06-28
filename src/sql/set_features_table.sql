CREATE OR REPLACE TABLE features AS 
SELECT 
    sku,
    dt_submitted,
    quantity_sold,
    EXTRACT(DAY FROM dt_submitted) AS day,
    EXTRACT(YEAR FROM dt_submitted) AS year,
    EXTRACT(MONTH FROM dt_submitted) AS month,
    EXTRACT(DOW FROM dt_submitted) AS day_of_week,
    EXTRACT(DOY FROM dt_submitted) AS day_of_year,
    EXTRACT(WEEK FROM dt_submitted) AS week_of_year,
    CASE 
        WHEN EXTRACT(DOW FROM dt_submitted) >= 5 THEN TRUE 
        ELSE FALSE 
    END AS is_weekend,
    COALESCE(LAG(quantity_sold, 1) OVER (PARTITION BY sku ORDER BY dt_submitted), 0) AS quantity_sold_lag_1,
    COALESCE(LAG(quantity_sold, 7) OVER (PARTITION BY sku ORDER BY dt_submitted), 0) AS quantity_sold_lag_7,
    COALESCE(AVG(quantity_sold) OVER (
        PARTITION BY sku 
        ORDER BY dt_submitted 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 0) AS rolling_mean_7
FROM data
