from pydantic import BaseModel, Field

#for validations


class Product(BaseModel):
    name: str = Field(..., example='iPhone 12')
    description: str = Field(None, example='iPhone 12 new model')
    price: float = Field(..., example=1100)