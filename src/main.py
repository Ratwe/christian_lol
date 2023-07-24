from fastapi import FastAPI, Depends

from src.auth.models import User
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.lol.lol import *
from src.lol.routers import router as router_lol

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

