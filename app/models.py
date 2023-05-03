from sqlalchemy import Column, Integer, ForeignKey, String

from app.db import Base


class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    screen_name: str = Column(String(length=255), nullable=False)
    profile_image: str | None = Column(String(length=255), nullable=True)


class Tweets(Base):
    id = Column(Integer, primary_key=True, index=True)
    sender_id: int = Column(ForeignKey("users.id", ondelete="CASCADE"))
    text: str = Column(String(length=255), nullable=False)
    timestamp: int = Column(Integer, nullable=False)


class Follows(Base):
    id = Column(Integer, primary_key=True, index=True)
    follower_id: int = Column(ForeignKey("users.id", ondelete="CASCADE"))
    followee_id: int = Column(ForeignKey("users.id", ondelete="CASCADE"))
