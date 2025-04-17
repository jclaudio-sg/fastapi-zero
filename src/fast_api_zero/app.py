from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_api_zero.schema import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

# banco de dados fake
database = []


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Ola mundo!'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    userDB = UserDB(
        id=(len(database) + 1),
        # Pega os dados do UserSchema e retorna um dicionario com esses dados.
        **user.model_dump(),
    )
    database.append(userDB)
    return userDB


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado'
        )
    user_with_id = database[user_id - 1]
    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrado'
        )
    del database[user_id - 1]
    return {'message': 'User deleted'}
