import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']
if __name__ == '__main__':
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1")
    with Connection(redis.from_url(os.environ['REDISTOGO_URL'])):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2")
        worker = Worker(map(Queue, listen))
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3")
        worker.work()

