from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status


def show_all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def show_single_blog(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")

    return blog


def create_blog(request: schemas.Blog, db: Session, email: str):
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=get_current_user_id(db, email))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def update_blog(id, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")
    blog.update(request.model_dump())
    db.commit()
    return "Updated"


def delete_blog(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deleted"


def get_current_user_id(db, email):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user.id
