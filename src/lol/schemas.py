from pydantic import BaseModel


class OperationCreate(BaseModel):
    match_id: str
    region: str = 'RU'
