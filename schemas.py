from typing import Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(..., example='iPhone 12')
    description: str = Field(None, example='iPhone 12 new model')
    price: float = Field(..., example=1100.00)


class Seller(BaseModel):
    username: str = Field(...,example='seller')
    email: str = Field(...,example='email@server.com')
    password: str = Field(...,example='123456')


class DisplaySeller(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class DisplayProduct(BaseModel):
    name: str
    description: str
    seller: DisplaySeller

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str = Field(..., example='seller')
    password: str = Field(..., example='123456')

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
