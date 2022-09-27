# used to create in DB
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    seller_id = Column(Integer, ForeignKey('sellers.id'))  # foreign key to seller table
    seller = relationship('Seller', back_populates='products')  # relationship to seller table


class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship('Product', back_populates='seller')  # relationship to product table

