import os

import django
import redis
from redis import Redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']


redis_url = os.getenv('REDISTOGO_URL')
print ('redis_url -> ' + str (redis_url))

if not redis_url:
    redis = Redis('localhost', 6379)
    conn = redis
else:
    conn = redis.from_url(redis_url)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studio_webapp.settings")
    django.setup(set_prefix=False)

    with Connection(conn):
        print ('connection queue')
        worker = Worker(map(Queue, listen))
        worker.work()


if __name__ == '__main__':
    main()
