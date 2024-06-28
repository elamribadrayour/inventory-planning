from pydantic import BaseModel

from api.models.output import Output


class Outputs(BaseModel):
    value: list[Output]

    class Config:
        json_schema_extra = {
            "example": {
                "value": [
                    {
                        "sku": "ABC123",
                        "quantity_sold_min": 10.5,
                        "quantity_sold_max": 20.0,
                    },
                    {
                        "sku": "XYZ456",
                        "quantity_sold_min": 5.0,
                        "quantity_sold_max": 15.0,
                    },
                ]
            }
        }
