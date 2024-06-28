import os
import json
import logging
from typing import Literal
from datetime import datetime, UTC

import joblib
import pandas
from sklearn.pipeline import Pipeline


def save_item(
    cache_dir: str,
    x: pandas.DataFrame,
    type_: Literal["train", "test"],
) -> None:
    folder_path = os.path.join(cache_dir, f"datasets/type={type_}")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "result.parquet")
    logging.info(f"save dataset to {file_path}")

    x.to_parquet(
        path=file_path,
        compression="gzip",
        engine="pyarrow",
    )


def save_data(
    cache_dir: str,
    df_test: pandas.DataFrame,
    df_train: pandas.DataFrame,
) -> None:
    save_item(cache_dir=cache_dir, x=df_test, type_="test")
    save_item(cache_dir=cache_dir, x=df_train, type_="train")


def save_model(cache_dir: str, model_name: str, model: Pipeline) -> None:
    exec_date = datetime.now(UTC).strftime("%Y-%m-%d-%H-%M-%S")
    folder_path = os.path.join(
        cache_dir, f"models/model={model_name}/exec_date={exec_date}"
    )
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "result.joblib")
    logging.info(f"save model to {file_path}")
    joblib.dump(value=model, filename=file_path)


def save_metrics(
    x: dict,
    cache_dir: str,
    exec_date: str,
    model_name: str,
) -> None:
    folder_path = os.path.join(
        cache_dir, f"metrics/model={model_name}/exec_date={exec_date}"
    )
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "result.json")
    logging.info(f"save metrics to {file_path}")
    with open(file_path, mode="w") as f:
        json.dump(x, f)


def save_results(
    cache_dir: str,
    x: pandas.DataFrame,
) -> None:
    exec_date = datetime.now(UTC).strftime("%Y-%m-%d-%H-%M-%S")
    folder_path = os.path.join(cache_dir, f"results/exec_date={exec_date}")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "result.parquet")
    logging.info(f"save results to {file_path}")
    x.to_parquet(
        path=file_path,
        compression="gzip",
        engine="pyarrow",
    )
