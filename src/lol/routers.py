from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.lol.lol import get_match_by_id, collect_match_info, get_summoner_by_name, get_summoner_mastery, \
    get_summoner_matches
from src.lol.models import match, match_res
from src.lol.schemas import OperationCreate

MINUTE = 60

router = APIRouter(
    prefix="/lol",
    tags=["lol"]
)


# ----------------------------------------------------------------------
@router.get("/users/{user_name}")
def get_user_by_name(user_name: str, region: str = 'ru'):
    return get_summoner_by_name(user_name, region)


# Информация о мастерстве топ-limit персонажей игрока по мастерству
@router.get("/users/{user_name}/mastery")
def get_user_mastery_by_name(user_name: str, region: str = 'ru', limit: int = 3):
    user_data = get_summoner_by_name(user_name, region)
    user_id = user_data["id"]
    mastery_data = get_summoner_mastery(user_id, region)
    return mastery_data[:limit]


# Матчи игрока
@router.get("/users/{user_name}/matches")
def get_user_matches_by_name(user_name: str, region: str = 'ru', limit: int = 5):
    user_data = get_summoner_by_name(user_name, region)
    user_puuid = user_data["puuid"]
    matches_data = get_summoner_matches(user_puuid, region, limit)
    return matches_data


# Информация о матче по id
@router.get("/{match_id}")
def get_match_info_by_id(match_id: str, region: str = 'ru'):
    match_data = get_match_by_id(match_id, region)
    return match_data


@router.get("/get_match")
async def get_specific_match(session: AsyncSession = Depends(get_async_session)):
    print("get_specific_match")
    query = select(match).where(match.c.game_duration >= 20 * MINUTE)
    result = await session.execute(query)
    await session.commit()

    return {
        "status": "success",
        "data": result.scalars().all(),
        "details": None
    }


@router.post("/{match_id}/add")
async def add_specific_match(match_id: str, region: str = 'ru', session: AsyncSession = Depends(get_async_session)):
    new_match = OperationCreate(match_id=match_id, region=region)
    data = get_match_by_id(**new_match.dict())

    metadata = data["metadata"]
    match_id = metadata["matchId"]
    info = data["info"]
    game_duration = info["gameDuration"]

    stmt = insert(match).values(match_id=match_id, game_duration=game_duration)
    await session.execute(stmt)
    await session.commit()

    return {
        "status": "success",
        "data": f"match_id={match_id}, game_duration={game_duration}",
        "details": None
    }


@router.post("/{match_id}/res")
async def calculate_match_res(match_id: str, region: str = 'ru', session: AsyncSession = Depends(get_async_session)):
    try:
        new_match = OperationCreate(match_id=match_id, region=region)
        data = collect_match_info(**new_match.dict())

        stmt = insert(match_res).values(min_kills=data["min_kills"],
                                        max_kills=data["max_kills"],
                                        min_deaths=data["min_deaths"],
                                        max_deaths=data["max_deaths"],
                                        min_assists=data["min_assists"],
                                        max_assists=data["max_assists"])
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e),
        })
