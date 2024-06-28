"""lifespan definition."""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sklearn.pipeline import Pipeline
from duckdb import DuckDBPyConnection

import helpers.download

metrics: dict
model: Pipeline
con: DuckDBPyConnection


async def init() -> None:
    """initialize api global variables."""
    global con, model, metrics

    logging.info("initialize model")
    model = helpers.download.get_model(
        cache_dir=os.environ["CACHE_DIR"],
        exec_date=os.environ["EXEC_DATE"],
        model_name=os.environ["MODEL_NAME"],
    )

    logging.info("initialize db")
    con = helpers.download.get_db(
        cache_dir=os.environ["CACHE_DIR"],
    )

    logging.info("initialize intervals")
    metrics = helpers.download.get_metrics(
        cache_dir=os.environ["CACHE_DIR"],
        exec_date=os.environ["EXEC_DATE"],
        model_name=os.environ["MODEL_NAME"],
    )


async def close() -> None:
    """delete api global variables."""
    global con, model, metrics

    con.close()
    del model, metrics


@asynccontextmanager
async def lifespan(_: FastAPI):
    """create api lifespan."""
    await init()
    yield
    await close()
