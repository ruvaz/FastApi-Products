from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routers.login import get_current_user

router = APIRouter(
    prefix='/api/product',
    tags=['Product']
)


# Create product
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayProduct)
def add_product(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Read all products
@router.get('/', response_model=List[schemas.DisplayProduct])
def get_products(
        db: Session = Depends(get_db),
        current_user: schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products  # return list of products


# Show product by id
@router.get('/product/{id}', response_model=schemas.DisplayProduct)
def get_product(id, db: Session = Depends(get_db),
                current_user: schemas.Seller = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id {id} not found')
    return product  # return product by id


@router.delete('/product/{id}')
def delete_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return product


@router.put('/product/{id}')
def update_product(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        return {'message': 'Product not found'}

    product.update(request.dict())
    db.commit()
    return {'message': 'Product updated', 'Product': product.first()}
