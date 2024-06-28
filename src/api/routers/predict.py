from fastapi import APIRouter, Security
from fastapi.responses import ORJSONResponse

import helpers.auth
import helpers.predict
import helpers.lifespan

from api.models.inputs import Inputs

router = APIRouter(
    tags=["Model"],
    dependencies=[Security(helpers.auth.check)],
)


@router.post(path="/predict")
def predict(inputs: Inputs) -> ORJSONResponse:
    predictions = helpers.predict.get_prediction(
        inputs=inputs,
        con=helpers.lifespan.con,
        model=helpers.lifespan.model,
        metrics=helpers.lifespan.metrics,
    )
    return ORJSONResponse(content=predictions.model_dump()["value"])
