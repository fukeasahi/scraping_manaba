import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']
if __name__ == '__main__':
    with Connection(redis.from_url(os.environ['REDISTOGO_URL'])):
        worker = Worker(map(Queue, listen))
        worker.work()