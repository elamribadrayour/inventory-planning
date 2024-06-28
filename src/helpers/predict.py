from datetime import datetime

import pandas
from sklearn.pipeline import Pipeline
from duckdb import DuckDBPyConnection

from api.models.output import Output
from api.models.inputs import Inputs
from api.models.outputs import Outputs


def get_features(con: DuckDBPyConnection, skus: list[str]) -> pandas.DataFrame:
    current_datetime = datetime.now()
    current_date_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    skus_str = ",".join([f"'{sku}'" for sku in skus])
    query = (
        open("sql/set_skus_features.sql")
        .read()
        .format(
            skus_str=skus_str,
            current_date_str=current_date_str,
        )
    )

    return con.execute(query).fetchdf().sort_values(by="sku")


def get_prediction(
    model: Pipeline, con: DuckDBPyConnection, metrics: dict, inputs: Inputs
) -> Outputs:
    skus = sorted(inputs.skus)

    features = get_features(
        con=con,
        skus=skus,
    )
    if len(features) == 0:
        return Outputs(
            value=[
                Output(sku=sku, quantity_sold_min=None, quantity_sold_max=None)
                for sku in inputs.skus
            ]
        )

    outputs = model.predict(X=features)
    outputs = [
        (
            max(0, int(output - metrics["mae"])),
            int(output + metrics["mae"]),
        )
        for output in outputs
    ]

    return Outputs(
        value=[
            Output(sku=sku, quantity_sold_min=output[0], quantity_sold_max=output[1])
            for sku, output in zip(inputs.skus, outputs)
        ]
    )
