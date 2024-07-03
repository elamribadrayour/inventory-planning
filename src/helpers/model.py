from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit


def get_xgboost_regression() -> RandomizedSearchCV:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                "passthrough",
                [
                    "day",
                    "year",
                    "month",
                    "is_weekend",
                    "day_of_year",
                    "day_of_week",
                    "week_of_year",
                    "rolling_mean_7",
                    "quantity_sold_lag_1",
                    "quantity_sold_lag_7",
                ],
            ),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["sku"]),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", XGBRegressor(random_state=42)),
        ]
    )

    param_dist = {
        "regressor__max_depth": [3, 5, 7, 9, 11],
        "regressor__subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
        "regressor__learning_rate": [0.01, 0.05, 0.1, 0.15],
        "regressor__n_estimators": [100, 200, 300, 400, 500],
        "regressor__colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
    }

    tscv = TimeSeriesSplit(n_splits=5)

    return RandomizedSearchCV(
        model,
        param_dist,
        n_iter=50,
        cv=tscv,
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
        verbose=0,
        random_state=42,
    )


def get_linear_regression() -> RandomizedSearchCV:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                "passthrough",
                [
                    "day",
                    "year",
                    "month",
                    "is_weekend",
                    "day_of_year",
                    "day_of_week",
                    "week_of_year",
                    "rolling_mean_7",
                    "quantity_sold_lag_1",
                    "quantity_sold_lag_7",
                ],
            ),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["sku"]),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression()),
        ]
    )

    tscv = TimeSeriesSplit(n_splits=5)

    return RandomizedSearchCV(
        model,
        dict(),
        n_iter=10,
        cv=tscv,
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
        verbose=0,
        random_state=42,
    )


def get_model(name: str) -> RandomizedSearchCV:
    if name == "xgboost-regressor":
        return get_xgboost_regression()
    elif name == "linear-regressor":
        return get_linear_regression()
    raise NotImplementedError(f"model provided doesn't exist {name}")
