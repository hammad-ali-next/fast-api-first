from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..hashing import Hash


def show_single_user(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    return user


def create_user(request: schemas.User, db: Session):
    password = request.password
    if len(password) >= 6 and password.isalnum():
        new_user = models.User(
            name=request.name, email=request.email, password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Password! \nPassword length should be equal or greater then 6 and should only contain Alphabet and Number")


def get_users_blogs(db, email):
    blogs = db.query(models.Blog).filter(models.Blog.user_id ==
                                         get_current_user_id(db, email)).all()
    return blogs


def get_current_user_id(db, email):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user.id
