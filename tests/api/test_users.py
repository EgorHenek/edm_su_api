import pytest
from httpx import AsyncClient
from starlette import status

from app.schemas.user import CreateUser, UserPassword, User, MyUser, Token
from tests.helpers import create_auth_header


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    new_user = CreateUser(
        password='testpassword',
        password_confirm='testpassword',
        username='TestUser',
        email='testuser@example.com',
    )
    response = await client.post('/users/', data=new_user.json())

    assert response.status_code == status.HTTP_200_OK
    assert MyUser.validate(response.json())
    assert response.json()['is_admin'] == False


@pytest.mark.asyncio
async def test_activate_user(client: AsyncClient, non_activated_user):
    url = f'/users/activate/{non_activated_user["activation_code"]}'
    response = await client.post(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_login(client: AsyncClient, admin: dict):
    response = await client.post(
        '/users/token',
        data={
            'username': admin['username'],
            'password': 'password',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert Token.validate(response.json())


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, admin: dict):
    response = await client.get(
        '/users/me',
        headers=create_auth_header(admin['username']),
    )

    assert response.status_code == status.HTTP_200_OK
    assert MyUser.validate(response.json())


@pytest.mark.asyncio
async def test_request_recovery_user(client: AsyncClient, admin: dict):
    response = await client.post(f'/users/password-recovery/{admin["email"]}')

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, admin: dict):
    data = {
        'new_password': {
            'password': 'newpassword',
            'password_confirm': 'newpassword',
        },
        'old_password': 'password',
    }
    response = await client.put(
        '/users/password',
        headers=create_auth_header(admin['username']),
        json=data,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_reset_password(client: AsyncClient, recovered_user_code: str):
    data = UserPassword(password='newpassword', password_confirm='newpassword')
    url = f'/users/reset-password/{recovered_user_code}'
    response = await client.put(url, data=data.json())

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_read_user(client: AsyncClient, admin: dict):
    response = await client.get(f'/users/{admin["id"]}')

    assert response.status_code == status.HTTP_200_OK
    assert User.validate(response.json())
