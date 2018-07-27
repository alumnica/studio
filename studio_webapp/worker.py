import os

import django
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL',
                      'redis://redistogo:0f33f80c90ba9c5b5ebd7dd4029c1a65@angelfish.redistogo.com:10112/')

conn = redis.from_url(redis_url)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studio_webapp.settings")
    django.setup(set_prefix=False)

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


if __name__ == '__main__':
    main()
