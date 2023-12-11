from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dependencies.database import get_db
from app.dependencies.models import Blog, Vote
from app.dependencies.schemas import CreatePost, PostResponse, UpdatePost, CreateUser, PostOut
from .authentication import get_current_user
import jsonify
import json

router = APIRouter(
    tags=['Blog'],
    prefix='/blog'
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(request: CreatePost, db: Session = Depends(get_db),
                      current_user = Depends(get_current_user)):
    query_title = db.query(Blog).filter(Blog.title == request.title).first()
    query_content = db.query(Blog).filter(Blog.content == request.content).first()
    if query_title or query_content:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Post already exist') 
    post = Blog(owner_id=current_user.id, **request.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# @router.get('/')
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def get_all_posts(db: Session = Depends(get_db), limit: int = 10, offset: int = 0, search: Optional[str] = "",
                        current_user: CreateUser = Depends(get_current_user)):
    title = db.query(Blog).filter(Blog.title.contains(search)).offset(offset).limit(limit).all()
    content = db.query(Blog).filter(Blog.content.contains(search)).offset(offset).limit(limit).all()
    
    # result = db.query(Blog, func.count(Vote.blog_id).label("votes")).join(
    #     Vote, Vote.blog_id == Blog.id, isouter=True).group_by(Blog.id).all()    
    
    # return result
    return title and content

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_post_by_id(id: int, db: Session = Depends(get_db),
                         current_user: CreateUser = Depends(get_current_user)):
    post = db.query(Blog).filter(Blog.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id({id}) not found')
    return post

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
async def update_post(id: int, request: UpdatePost, db: Session = Depends(get_db),
                      current_user: CreateUser = Depends(get_current_user)):
    post = db.query(Blog).filter(Blog.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id({id}) not found')
    if current_user.id != post.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this operation")
    post.title = request.title
    post.content = request.content
    db.commit()
    db.refresh(post)
    return post
 
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user: CreateUser = Depends(get_current_user)):
    query = db.query(Blog).filter(Blog.id == id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id({id}) not found')
    if current_user.id != query.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this operation")
    db.delete(query)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
