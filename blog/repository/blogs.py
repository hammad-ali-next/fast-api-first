from typing import Optional
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status


def show_all_blogs(db: Session, category: Optional[str] = None):
    query = db.query(models.Blog)
    if category:
        query = query.filter(models.Blog.category == category.lower())

    blogs = query.all()
    return blogs  # Always return the list, even if it's empty


def show_single_blog(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")

    return blog


def create_blog(request: schemas.CreateBlog, db: Session, email: str):
    user_id = get_current_user_id(db, email)
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        category=request.category,
        image_base64=request.image_base64,
        user_id=user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def blogs_update(id: int, request: schemas.UpdateBlog, db: Session, current_user: schemas.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found",
        )

    # Optional: check if current_user owns this blog (authorization)
    # if blog.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to update this blog")

    # Update only provided fields
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(blog, key, value)

    db.commit()
    # refresh to get updated blog data if you want to return it
    db.refresh(blog)

    return {"message": "Blog updated successfully", "blog": blog}


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
