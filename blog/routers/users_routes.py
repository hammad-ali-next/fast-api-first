from fastapi import APIRouter, Depends, HTTPException, status

from blog.hashing import Hash
from blog.routers.blogs_routes import get_current_user_id
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import users
from ..oauth2 import get_current_user
from typing import List
from prisma import Prisma

router = APIRouter(
    prefix='/users',
    tags=['users']
)


# =-=-=-= GET =-=-=-= #

# @router.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
# def get_current_users_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return users.get_users_blogs(db, current_user.email)

@router.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
async def get_current_users_blogs(current_user: schemas.User = Depends(get_current_user)):
    db = Prisma()
    user_id = await get_current_user_id(current_user.email)
    await db.connect()
    blogss = await db.blogs.find_many(
        where={
            'user_id': user_id
        },
        include={
            'creator': True
        }
    )

    await db.disconnect()
    return blogss


# @router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
# def show_single_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return users.show_single_user(id, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
async def show_single_user(id: int, current_user: schemas.User = Depends(get_current_user)):
    db = Prisma()
    await db.connect()
    user = await db.users.find_first(
        where={
            'id': id,
        },
        include={
            'blogs': True
        }
    )
    return user


# =-=-=-= POST =-=-=-= #

# @router.post('/register', response_model=schemas.ShowUser)
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     return users.create_user(request, db)


@router.post('/register', response_model=schemas.ShowUser)
async def create_user(request: schemas.User):
    db = Prisma()
    password = request.password
    if len(password) >= 6 and password.isalnum():
        await db.connect()

        new_user = await db.users.create(data={
            'name': request.name,
            'email': request.email,
            'password': Hash.bcrypt(request.password)
        })
        await db.disconnect()
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Password! \nPassword length should be equal or greater then 6 and should only contain Alphabet and Number")
