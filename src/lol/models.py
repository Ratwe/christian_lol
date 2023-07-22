from typing import List

from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()


class Participants:
    championName: str
    championId: int


class MatchInfo:
    id: int
    gameDuration: int
    participants: List[Participants]


match = Table(
    "match",
    metadata,
    Column("match_id", String, primary_key=True, nullable=False),
    Column("game_duration", Integer, nullable=False),
)