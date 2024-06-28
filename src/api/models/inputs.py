from pydantic import BaseModel


class Inputs(BaseModel):
    skus: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "skus": [
                    "-1079705109983218228",
                    "-1025753159201624061",
                    "-129295609970996479",
                ]
            }
        }
