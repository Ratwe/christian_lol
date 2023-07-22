from fastapi import FastAPI, Depends

from src.auth.models import User
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.lol.lol import *
from src.lol.router import router as router_lol

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_lol)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def protected_route():
    return f"Hello, stranger!"


fake_users = []


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    cur_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
    cur_user["name"] = new_name
    return {"status": 200, "data": cur_user}


# ----------------------------------------------------------------------
@app.get("/users/{user_name}")
def get_user_by_name(user_name: str, region: str = 'ru'):
    return get_summoner_by_name(user_name, region)


# Информация о мастерстве топ-limit персонажей игрока по мастерству
@app.get("/users/{user_name}/mastery")
def get_user_mastery_by_name(user_name: str, region: str = 'ru', limit: int = 3):
    user_data = get_summoner_by_name(user_name, region)
    user_id = user_data["id"]
    mastery_data = get_summoner_mastery(user_id, region)
    return mastery_data[:limit]


# Матчи игрока
@app.get("/users/{user_name}/matches")
def get_user_matches_by_name(user_name: str, region: str = 'ru', limit: int = 5):
    user_data = get_summoner_by_name(user_name, region)
    user_puuid = user_data["puuid"]
    matches_data = get_summoner_matches(user_puuid, region, limit)
    return matches_data


# Информация о матче по id
@app.get("/matches/{match_id}")
def get_match_info_by_id(match_id: str, region: str = 'ru'):
    match_data = get_match_info(match_id, region)
    return match_data
