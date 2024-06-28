"""train model for inventory planning prediction."""

import logging

import pandas
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV


def train(
    grid_search: GridSearchCV,
    x_train: pandas.DataFrame,
    y_train: pandas.DataFrame,
) -> Pipeline:
    grid_search.fit(X=x_train, y=y_train)

    best_params = grid_search.best_params_
    best_score = -grid_search.best_score_
    logging.info(f"Best Parameters: {best_params}")
    logging.info(f"Best Mean Absolute Error: {best_score}")

    return grid_search.best_estimator_
