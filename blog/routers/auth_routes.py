from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..repository import blogs
from .. hashing import Hash
from ..token import create_access_token

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Email!")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Password!")
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)

    return {"message": "Login successful"}
