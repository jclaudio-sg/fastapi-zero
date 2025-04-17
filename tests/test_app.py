from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # 2. Act - Ação
    assert response.status_code == HTTPStatus.OK  # 3. Assert
    assert response.json() == {'message': 'Ola mundo!'}  # 3. Assert


def test_create_user(client):
    response = client.post(  # 2. Ação
        '/users/',
        json={
            'username': 'maria',
            'email': 'mar@gmail.com',
            'password': '1234',
        },
    )

    # Voltou status code correto ?
    assert response.status_code == HTTPStatus.CREATED
    # Validou UserSchema
    assert response.json() == {
        'username': 'maria',
        'email': 'mar@gmail.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'maria',
                'email': 'mar@gmail.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(  # 2. Ação
        '/users/1',
        json={
            'username': 'maria',
            'email': 'mar@gmail.com',
            'password': '1234',
        },
    )
    assert response.json() == {
        'username': 'maria',
        'email': 'mar@gmail.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'maria',
        'email': 'mar@gmail.com',
        'id': 1,
    }
