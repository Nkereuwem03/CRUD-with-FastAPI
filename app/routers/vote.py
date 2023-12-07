from fastapi import APIRouter, Depends, HTTPException, status
from .authentication import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.dependencies.database import get_db
from app.dependencies.schemas import AddVote
from app.dependencies.models import Vote, Blog

router = APIRouter(
    prefix='/vote',
    tags=['vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(request: AddVote, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = db.query(Blog).filter(Blog.id == request.blog_id).first()
    query_vote = db.query(Vote).filter(and_(Vote.user_id == current_user.id, Vote.blog_id == request.blog_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id={request.blog_id} does not exit')
    if request.dir == 1:
        if query_vote:
            # no_of_votes = db.query(Vote).filter(Vote.blog_id == request.blog_id).count()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'User {current_user.id} has already voted on post {request.blog_id}')
        vote = Vote(user_id = current_user.id, blog_id = request.blog_id)
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return {'message': 'successfully added vote'}  
    else:
        if not query_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No vote found")
        db.delete(query_vote)
        db.commit()
        return {'message': 'successfully deleted vote'}
        
