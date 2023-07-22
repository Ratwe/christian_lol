from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.lol.models import match

MINUTE = 60

router = APIRouter(
    prefix="/lol",
    tags=["lol"]
)


@router.get("/")
async def get_specific_match(session: AsyncSession = Depends(get_async_session)):
    query = select(match).where(match.c.game_duration >= 20 * MINUTE)
    result = await session.execute(query)
    return result.all()

@router.get("/")
async def add_specific_match(match_id: int, session: AsyncSession = Depends(get_async_session)):
    
    return {"status": "success"}