from turtle import title
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas import Post, PostCreate, PostSchema
from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.get('/',response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/',response_model=PostSchema)
def create_post(post: PostSchema, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=PostSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    print(post)
    return post


@router.put('/{id}')
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):

    single_post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = single_post_query.first()
    
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can't update post with id: {id} not found")

    update_post = single_post_query.update(post.dict(), synchronize_session=False)

    db.commit()
    return single_post_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can't delete post with id: {id} not found")
    
    delete_post.delete(synchronize_session=False)
    db.commit()
    return {'message': "Post Deleted"}
