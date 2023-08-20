from httpx import AsyncClient


async def test_get_user_by_name(ac: AsyncClient):
    response = await ac.get("/lol/users/Dundа")

    assert response.status_code == 200
    assert response.json()["id"] == "ZzFNjzIAyVbcEHgjI4bRtAI22O6qt1BuqQLJg7-ydTrUDVw"
    assert response.json()["accountId"] == "sIyJk86q5T_fKv7U0ZQhitMm8I4POCi0DQ4fM360zLCBPXE1jMpCuE8L"
    assert response.json()["puuid"] == "GuQ-qlbcxSLSyfz-AjuxSqjztTb1fxT1gY6BfseXWiQwzz8iNoAY5QYxrwTiM2x4Azx22yw0NwKsTg"


async def test_get_user_mastery_by_name(ac: AsyncClient):
    response = await ac.get("/lol/users/Dundа/mastery")

    assert response.status_code == 200
    assert response.json()[0]["summonerId"] == "ZzFNjzIAyVbcEHgjI4bRtAI22O6qt1BuqQLJg7-ydTrUDVw"
    assert response.json()[0][
               "puuid"] == "GuQ-qlbcxSLSyfz-AjuxSqjztTb1fxT1gY6BfseXWiQwzz8iNoAY5QYxrwTiM2x4Azx22yw0NwKsTg"


async def test_get_user_matches_by_name(ac: AsyncClient):
    response = await ac.get("/lol/users/Dundа/matches")

    assert response.status_code == 200


async def test_get_match_info_by_id(ac: AsyncClient):
    response = await ac.get("/lol/RU_455279141")

    assert response.status_code == 200


async def test_add_specific_match(ac: AsyncClient):
    response = await ac.post("/lol/add/RU_455279141")

    assert response.status_code == 200
    assert response.json()["status"] == "success"



async def test_calculate_match_res(ac: AsyncClient):
    response = await ac.post("/lol/res/RU_455279141")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
