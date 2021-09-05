import os

import redis
from rq import Worker, Connection

print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1")
with Connection(redis.from_url(os.environ['REDISTOGO_URL'])):
  print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2")
  worker = Worker(['default'])
  print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3")
  worker.work()