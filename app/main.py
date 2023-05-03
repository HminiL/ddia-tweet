from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette import status

from app import services, schemas
from app.db import get_db

app = FastAPI()


@app.get(
    "/timeline/{user_id}",
    response_model=list[schemas.Tweet],
    status_code=status.HTTP_200_OK,
)
async def get_timeline(
    user_id: int,
    db: Session = Depends(get_db),
) :
    tweets = services.get_timeline(user_id, db)
    return tweets


@app.post(
    "/tweet"
)
async def tweet(tweet_req: schemas.TweetIn,  db: Session = Depends(get_db)):
    services.set_tweets(tweet_req, db)
    return {"message": "Tweet created successfully", "status": status.HTTP_201_CREATED}
