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
        assert result.all() == [(1, 'admin', None)], "Role didn't add"


def test_register():
    print("_response beginning")

    json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    }

    print(f"json = {json}")
    response = client.post("/auth/register", json=json)

    print("response = ", response)
    assert response.status_code == 201
