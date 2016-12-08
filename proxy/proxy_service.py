import redis
import json
from flask import Flask

proxy_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)

COUNTER = 0
PROXIES_COUNT = 0


@proxy_service.route("/next_proxy")
def next_proxy():
    global COUNTER
    COUNTER += 1
    p = r.get('proxy:' + str(COUNTER % PROXIES_COUNT))
    return json.loads(p)


def init():
    global PROXIES_COUNT
    PROXIES_COUNT = len(r.hgetall("proxy:*"))


if __name__ == "__main__":
    proxy_service.run()
