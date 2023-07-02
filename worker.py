from os import environ as env

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = str(env.get('REDIS_URL'))

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
