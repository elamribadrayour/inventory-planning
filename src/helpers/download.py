"""download helpers."""

import os
import json
from typing import Literal

import joblib
import pandas
import duckdb
from duckdb import DuckDBPyConnection
from sklearn.pipeline import Pipeline


def get_item(
    cache_dir: str,
    type_: Literal["train", "test"],
) -> pandas.DataFrame:
    file_path = os.path.join(cache_dir, f"datasets/type={type_}/result.parquet")
    if os.path.exists(file_path) is False:
        raise ValueError(f"File doesn't exist: {file_path}")
    return pandas.read_parquet(file_path)


def get_train_data(
    cache_dir: str,
) -> tuple[pandas.DataFrame, pandas.DataFrame]:
    data = get_item(cache_dir=cache_dir, type_="train")
    return data.drop(labels="quantity_sold", axis=1), data[["quantity_sold"]]


def get_test_data(
    cache_dir: str,
) -> tuple[pandas.DataFrame, pandas.DataFrame]:
    data = get_item(cache_dir=cache_dir, type_="test")
    return data.drop(labels="quantity_sold", axis=1), data[["quantity_sold"]]


def get_model(
    exec_date: str,
    cache_dir: str,
    model_name: str,
) -> Pipeline:
    file_path = os.path.join(
        cache_dir, f"models/model={model_name}/exec_date={exec_date}/result.joblib"
    )
    if os.path.exists(file_path) is False:
        raise ValueError(f"File doesn't exist: {file_path}")
    return joblib.load(filename=file_path)


def get_db(
    cache_dir: str,
) -> DuckDBPyConnection:
    file_path = os.path.join(cache_dir, "database/result.duckdb")
    if os.path.exists(file_path) is False:
        raise ValueError(f"File doesn't exist: {file_path}")
    return duckdb.connect(database=file_path)


def get_metrics(
    exec_date: str,
    cache_dir: str,
    model_name: str,
) -> dict:
    file_path = os.path.join(
        cache_dir, f"metrics/model={model_name}/exec_date={exec_date}/result.json"
    )
    if os.path.exists(file_path) is False:
        raise ValueError(f"File doesn't exist: {file_path}")

    with open(file_path, mode="r") as f:
        return json.load(f)
