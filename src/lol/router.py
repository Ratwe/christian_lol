from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.lol.lol import get_match_by_id, collect_match_info
from src.lol.models import match, match_res
from src.lol.schemas import OperationCreate

MINUTE = 60

router = APIRouter(
    prefix="/lol",
    tags=["lol"]
)


@router.get("/")
async def get_specific_match(session: AsyncSession = Depends(get_async_session)):
    query = select(match).where(match.c.game_duration >= 20 * MINUTE)
    result = await session.execute(query)
    # noinspection PyTypeChecker
    matches: list[str] = result.scalars().all()
    await session.commit()

    return {
        "status": "success",
        "data": matches,
        "details": None
    }



@router.post("/")
async def add_specific_match(new_match: OperationCreate, session: AsyncSession = Depends(get_async_session)):
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


@router.post("/calc")
async def calculate_match_res(new_match: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
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

