import pytest
from sqlalchemy import insert, select

from src.auth.models import role
from tests.conftest import async_session_maker, client


@pytest.mark.asyncio
async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        print(result.all())


def test_register():
    response = client.post("/auth/register", json={
        "email": "pytest_email",
        "password": "pytest_password",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "pytest_username",
        "role_id": 0
    })

    assert response.status_code == 201
