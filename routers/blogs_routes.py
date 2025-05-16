from fastapi import APIRouter, Depends, status
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Annotated
from ..repository import blogs
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)


# =-=-=-= GET =-=-=-= #
# 2 ways for defining dependecies
# db: Session = Depends(get_db)                          1st way
# db: Annotated[Session, Depends(get_db)]                2nd way


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def show_all_blogs(db: Annotated[Session, Depends(get_db)], current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return blogs.show_all_blogs(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show_single_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blogs.show_single_blog(id, db)


# =-=-=-= POST =-=-=-= #


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blogs.create_blog(request, db)

# =-=-=-= PUT =-=-=-= #


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blogs.update_blog(id, request, db)


# =-=-=-= DELETE =-=-=-= #


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blogs.delete_blog(id, db)
