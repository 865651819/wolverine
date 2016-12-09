import redis
import json
from flask import Flask

proxy_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)

STACK = []


@proxy_service.route("/next_proxy")
def next_proxy():
    return STACK.pop()


def init():
    for key in r.scan_iter('proxy:*'):
        STACK.append(r.get(key))


if __name__ == "__main__":
    init()
    proxy_service.run()
