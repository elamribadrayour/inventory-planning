CREATE OR REPLACE TABLE data AS 
SELECT 
    CAST(SKU AS STRING) AS sku, 
    CAST(DATE AS TIMESTAMP) AS dt_submitted, 
    CAST(QUANTITY_SOLD AS INT) AS quantity_sold
FROM read_csv_auto('{file_path}')
