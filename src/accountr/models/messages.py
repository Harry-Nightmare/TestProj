from datetime import date

from pydantic import BaseModel


class SimpleMessage(BaseModel):
    date: date
    payload: str


class MessageCreate(SimpleMessage):
    pass


class MessageUpdate(SimpleMessage):
    pass


class Message(SimpleMessage):
    id: int

    class Config:
        orm_mode = True
