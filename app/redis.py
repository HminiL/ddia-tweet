import json

import redis


redis_client: redis.Redis = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


def set_in_cache(key: str, value: str):
    redis_client.lpush(key, value)  # TODO: Modify lpush to lpushx when login is implemented


def get_from_cache(key: str) -> list:
    return [eval(message.decode()) for message in redis_client.lrange(key, 0, -1)]


# class RedisPubSub:
#     def __init__(self, host: str, port: int = 6379, db: int = 0):
#         self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
#         self.pubsub = self.redis_client.pubsub()
#
#     def subscribe(self, channel: str):
#         self.pubsub.subscribe(channel)
#         for message in self.pubsub.listen():
#             if message["type"] == "message":
#                 yield json.loads(message["data"])
#
#     def publish(self, channel: str, data: dict):
#         self.redis_client.publish(channel, json.dumps(data))
#
#
# redis_pubsub = RedisPubSub(host="localhost")
