from pydantic import BaseModel, Field

#for validations


class Product(BaseModel):
    name: str = Field(..., example='iPhone 12')
    description: str = Field(None, example='iPhone 12 new model')
    price: float = Field(..., example=1100.00)


class DisplayProduct(BaseModel):
    name: str
    description: str
    class Config:
        orm_mode = True


class Seller(BaseModel):
    username: str
    email: str
    password: str


class DisplaySeller(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True
