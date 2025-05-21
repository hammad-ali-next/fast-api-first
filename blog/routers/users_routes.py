from fastapi import APIRouter, Depends, status
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import users
from ..oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['users']
)


# =-=-=-= GET =-=-=-= #

@router.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.Blog])
def get_current_users_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return users.get_users_blogs(db, current_user.email)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def show_single_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return users.show_single_user(id, db)


# =-=-=-= POST =-=-=-= #

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return users.create_user(request, db)
