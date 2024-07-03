"""prepare training data."""

import os
import logging

import gdown
import pandas
import duckdb
from duckdb import DuckDBPyConnection
from sklearn.model_selection import train_test_split


def set_raw_table(cache_dir: str) -> DuckDBPyConnection:
    folder_path = os.path.join(cache_dir, "datasets/type=raw")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "data.csv")

    if os.path.exists(file_path) is False:
        logging.info("downloading file from gdrive")
        url = "https://drive.google.com/uc?id=1ZQ8Kj30A_heysk1NJlNLsFYJjkB7POQ0"
        gdown.download(url, file_path, quiet=False)

    folder_path = os.path.join(cache_dir, "database")
    os.makedirs(folder_path, exist_ok=True)

    db_path = os.path.join(folder_path, "result.duckdb")
    conn = duckdb.connect(database=db_path)
    conn.execute(open("sql/set_raw_table.sql").read().format(file_path=file_path))

    return conn


def set_features_table(con: DuckDBPyConnection) -> None:
    con.execute(open("sql/set_features_table.sql").read())


def get_train_test_split(
    con: DuckDBPyConnection,
) -> tuple[pandas.DataFrame, pandas.DataFrame]:
    data_frame = con.execute("SELECT * FROM features").fetch_df()

    test_list = list()
    train_list = list()

    unique_skus = data_frame["sku"].unique()

    for sku in unique_skus:
        sku_data = data_frame[data_frame["sku"] == sku].sort_values(by="dt_submitted")

        if len(sku_data) > 1:
            sku_train_data, sku_test_data = train_test_split(
                sku_data, test_size=0.2, random_state=42
            )
            train_list.append(sku_train_data)
            test_list.append(sku_test_data)
        else:
            train_list.append(sku_data)

    train_data = pandas.concat(train_list)
    test_data = pandas.concat(test_list)

    return train_data, test_data


def get_data(
    cache_dir: str,
) -> tuple[DuckDBPyConnection, pandas.DataFrame, pandas.DataFrame]:
    logging.info("build raw table in duckdb")
    con = set_raw_table(cache_dir=cache_dir)
    logging.info("build features table in duckdb")
    set_features_table(con=con)
    logging.info("build training & testing datasets")
    df_train, df_test = get_train_test_split(con=con)
    return con, df_train, df_test
