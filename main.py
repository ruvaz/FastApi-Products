from fastapi import FastAPI

from Product import schemas, models
from Product.database import engine

# uvicorn main:app --reload
app = FastAPI()

# create tables
models.Base.metadata.create_all(engine)

# routes for endpoints
@app.post('/product')
def product(request: schemas.Product):
    return request

