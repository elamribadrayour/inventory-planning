import pandas
from duckdb import DuckDBPyConnection
from sklearn.pipeline import Pipeline

import helpers.predict

from api.models.inputs import Inputs


def get_predictions(
    model: Pipeline, con: DuckDBPyConnection, metrics: dict
) -> pandas.DataFrame:
    skus = con.execute("SELECT DISTINCT sku FROM features").fetch_df()["sku"].tolist()
    results = helpers.predict.get_prediction(
        con=con,
        model=model,
        metrics=metrics,
        inputs=Inputs(skus=skus),
    )

    return pandas.DataFrame(data=results.model_dump()["value"])
