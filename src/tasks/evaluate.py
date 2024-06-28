"""Evaluate inventory planning model."""

import logging

import pandas
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    root_mean_squared_error,
)


def evaluate(
    model: Pipeline,
    x_test: pandas.DataFrame,
    y_test: pandas.DataFrame,
) -> dict:
    y_pred = model.predict(X=x_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    output = {
        "r2": r2,
        "mae": mae,
        "mse": mse,
        "rmse": rmse,
    }
    logging.info(output)
    return output
