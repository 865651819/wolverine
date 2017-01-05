import redis
from flask import Flask, request

proxy_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)

STACK = []


@proxy_service.route("/proxy")
def next_proxy():

    start = request.args.get('start')
    limit = request.args.get('limit')

    if len(STACK) <= 0:
        # TODO: add better logic to fix this
        init()
    return STACK.pop()


def init():
    for key in r.scan_iter('proxy:*'):
        STACK.append(r.get(key))


if __name__ == "__main__":
    init()
    proxy_service.run(host='localhost', port=5002)
