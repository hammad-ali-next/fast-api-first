from typing import Any, Optional
from fastapi import APIRouter, Depends, status

from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Annotated
from ..repository import blogs
from ..oauth2 import get_current_user
from prisma import Prisma


router = APIRouter(
    prefix='/blogs',
    tags=['blogs']
)


# =-=-=-= GET =-=-=-= #
# 2 ways for defining dependecies
# db: Session = Depends(get_db)                          1st way
# db: Annotated[Session, Depends(get_db)]                2nd way


# @router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
# # , current_user: Annotated[schemas.User, Depends(get_current_user)]):
# def show_all_blogs(
#         category: Optional[str] = None,
#         db: Session = Depends(get_db)):

#     return blogs.show_all_blogs(db, category)


@router.get('/')
async def show_all_blogs(category: Optional[str] = None):
    db = Prisma()
    await db.connect()

    # where: Any = None

    # if category:
    #     where = {'category': category}

    blogs = await db.blogs.find_many(
        where={'category': category} if category else None,
        include={'creator': True}
    )
    await db.disconnect()
    return blogs


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
# , current_user: schemas.User = Depends(get_current_user)):
def show_single_blog(id: int, db: Session = Depends(get_db)):
    return blogs.show_single_blog(id, db)


# =-=-=-= POST =-=-=-= #


# @router.post('/', status_code=status.HTTP_201_CREATED)
# def create_blog(request: schemas.CreateBlog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return blogs.create_blog(request, db, current_user.email)

async def get_current_user_id(email):
    db = Prisma()
    await db.connect()
    user = await db.users.find_first(
        where={
            'email': email,
        },)

    await db.disconnect()

    if user is None:
        raise ValueError(f"No user found with email: {email}")

    return user.id


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.CreateBlog, current_user: schemas.User = Depends(get_current_user)):
    db = Prisma()
    await db.connect()

    user_id = await get_current_user_id(current_user.email)
    new_blog = await db.blogs.create(data={
        'title': request.title,
        'body': request.body,
        'category': request.category,
        'image_base64': request.image_base64,
        'user_id': user_id
    },)

    await db.disconnect()
    return new_blog

# =-=-=-= PUT =-=-=-= #


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int,
    request: schemas.UpdateBlog,  # <-- use UpdateBlog schema
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return blogs.blogs_update(id, request, db, current_user)

# =-=-=-= DELETE =-=-=-= #


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blogs.delete_blog(id, db)
