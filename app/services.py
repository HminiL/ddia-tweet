from sqlalchemy import text
from sqlalchemy.orm import Session

from app.redis import set_in_cache, get_from_cache
from app.schemas import TweetIn


def _set_tweets_in_rdbms(tweet: TweetIn, db: Session):
    db.execute(
        text(
            """
            INSERT INTO tweets (sender_id, text, timestamp)
            VALUES (:sender_id, :text, :timestamp)
            """
        ),
        params={
            "sender_id": tweet.sender_id,
            "text": tweet.text,
            "timestamp": tweet.timestamp,
        },
    )
    db.commit()


def _set_timeline_in_cache(tweets: TweetIn, db: Session):
    followee_ids = db.execute(
        text(
            """
            SELECT followee_id FROM follows
            WHERE follower_id = :user_id
            """
        ),
        params={"user_id": tweets.sender_id},
    ).all()
    for followee_id in followee_ids:
        set_in_cache(f"timeline:{followee_id}", str(tweets))


def set_tweets(tweet: TweetIn, db: Session):
    _set_tweets_in_rdbms(tweet, db)
    _set_timeline_in_cache(tweet, db)


def _get_timeline_from_cache(user_id: int) -> list:
    tweets = get_from_cache(f"timeline:{user_id}")
    if not tweets:
        return []
    return tweets


def _get_timeline_from_rdbms(user_id: int, db: Session) -> list:
    tweets = db.execute(
        text(
            """
            SELECT tweets.* FROM tweets
            JOIN users on tweets.sender_id = users.id
            JOIN follows on follows.followee_id = users.id
            WHERE follows.follower_id = :user_id
            """
        ),
        params={"user_id": user_id},
    ).all()
    return tweets


def get_timeline(user_id: int, db: Session) -> list:
    tweets = _get_timeline_from_cache(user_id)
    if not tweets:
        tweets = _get_timeline_from_rdbms(user_id, db)
    return tweets
