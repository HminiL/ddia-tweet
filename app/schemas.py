from datetime import datetime

from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        orm_mode = True


class TweetIn(Base):
    sender_id: int
    text: str
    timestamp: datetime


class TweetOut(Base):
    id: int
    sender_id: int
    text: str
    timestamp: int

