import os

import redis
from rq import Worker, Connection

redis_url = os.environ['REDISTOGO_URL']
conn = redis.from_url(redis_url)
with Connection(conn):
    worker = Worker(['default'])
    worker.work()