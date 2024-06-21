from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOutput, UserOutputAll

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", status_code=201, response_model=UserOutput)
def user_create(user: UserCreate, db: Depends = Depends(get_db)):
    query = db.query(User).filter(User.username == user.username)
    if query.first() is not None:
        raise HTTPException(status_code=409, detail=f"This {user.username} is already registered.")

    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def user_create(chat_id: int, db: Depends = Depends(get_db)):
    query = db.query(User).filter(User.chat_id == chat_id)
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='User doesnt exists!')
    query.delete()
    db.commit()
    return "User has been removed"


# @router.patch('/{chat_id}', status_code=201, response_model=UserOutput)
# def update_my_user(chat_id: int, user_data: UserUpdate, db: Depends = Depends(get_db)):
#     query = db.query(User).filter(User.chat_id == chat_id)
#     user = query.first()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='User doesnt exists!')
#     query.update(user_data.dict(), synchronize_session=False)
#
#     db.commit()
#     return user


@router.get('/all', response_model=UserOutputAll)
def user_list(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}


@router.get('/search', response_model=UserOutputAll)
def get_user(q: str | None = None, db: Session = Depends(get_db)):
    # if q is None or q == '{q}':
    if not q:
        # user_list()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Search query cannot be empty')

    # Perform a case-insensitive substring search using SQLite's LIKE
    users = db.query(User).filter(or_(User.full_name.like(f"%{q}%"), User.username.like(f"%{q}%"))).all()

    # if not users:
    #     return {"error": 'User not found'}
        # raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='User not found')

    return {"users": users}


@router.get('/', response_model=UserOutput)
def get_user(chat_id: int, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.chat_id == chat_id)  # noqa
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='User doesnt exists!')
    return user
