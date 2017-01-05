from random import randint
import redis
import json
from flask import Flask

useragent_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)


@useragent_service.route('/useragent/<int:amount>')
def user_agent(amount):
    candidates = []
    index = 0
    while index < amount:
        candidates.append(r.get('ua:pc:' + str(randint(1, 9890))))
        index += 1
    return json.dumps(candidates)


if __name__ == "__main__":
    useragent_service.run(host='localhost', port=5001)
