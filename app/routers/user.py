from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.models import User
from app.dependencies.schemas import CreateUser, UserResponse, UpdateUser
from app.routers.authentication import get_current_user, pwd_context

router = APIRouter(
    tags=['User'],
    prefix='/user'
)

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def user(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication failed')
    return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(request: CreateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Email already exist')        
    user = User(username=request.username,
                email=request.email, password=pwd_context.hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user   

@router.get('/', response_model= List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
         
@router.get('/{username}', response_model=UserResponse)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username({username}) not found')
    return user

@router.put("/{username}", response_model=UserResponse)
async def update_user(username: str, request: UpdateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username({username}) not found')
    user.email = request.email
    db.commit()
    db.refresh(user)
    return user

@router.delete('/{username}')
async def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username({username}) not found')
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  