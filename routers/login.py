from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import models
import schemas
from database import get_db

router = APIRouter(
    prefix='/api/login',
    tags=['Login']
)

SECRET_KEY = 'e27HiciNPlydF1ghznpzYyj1ghn+rMXECzHWAqiOJFaS0A='
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 10  # 10 minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# to has passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/', response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid credentials'
        )
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Incorrect password'
        )
    access_token = generate_token(
        {
            "sub": seller.username,
            "seller_id": seller.id
        })
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        seller_id: int = payload.get("seller_id")

        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, seller_id=seller_id)
    except JWTError:
        raise credentials_exception
    return token_data
