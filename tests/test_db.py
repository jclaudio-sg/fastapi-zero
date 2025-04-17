from sqlalchemy import select

from fast_api_zero.models.models import User


def test_create_user(session):
    user = User(username='claudio', password='1234', email='claudio@gmail.com')
    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'claudio@gmail.com')
    )

    assert result.email == 'claudio@gmail.com'
