from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.configs.database import get_session
from fast_api_zero.models.models import User
from fast_api_zero.schema import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Ola mundo!'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.email == user.email)))

    if db_user:
        if db_user.email == user.email:
            # Email ja existe
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10,  # Limite a quantidade de registros.
    skip: int = 0,  # Informa de onde vai começar a consulta.
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    if user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado'
        )
    db_user = session.scalar(select(User).where(User.id == user_id))
    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    user_db.username = user.username
    user_db.password = user_db.password
    user_db.email = user.email

    session.commit()
    session.refresh(user_db)

    return user_db


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User nor found.'
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted.'}
