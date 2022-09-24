# used to create in DB
from sqlalchemy import Column, String, Integer, Float

from Product.database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

