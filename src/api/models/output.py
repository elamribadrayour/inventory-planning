from pydantic import BaseModel


class Output(BaseModel):
    sku: str
    quantity_sold_min: float | None
    quantity_sold_max: float | None

    class Config:
        json_schema_extra = {
            "example": {
                "quantity_sold_min": 10.5,
                "quantity_sold_max": 20.0,
                "sku": "-1025753159201624061",
            }
        }
