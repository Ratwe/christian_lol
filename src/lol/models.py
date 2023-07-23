from typing import List

from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

match = Table(
    "match",
    metadata,
    Column("match_id", String, primary_key=True, nullable=False),
    Column("game_duration", Integer, nullable=False),
)

match_res = Table(
    "match_res",
    metadata,
    Column("min_kills", String),
    Column("max_kills", String),
    Column("min_deaths", String),
    Column("max_deaths", String),
    Column("min_assists", String),
    Column("max_assists", String),
)