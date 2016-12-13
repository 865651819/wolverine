import random
import redis
from flask import Flask

useragent_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)


@useragent_service.route('/useragent')
def user_agent():
    random.seed()
    return str(r.get('ua:pc:' + str(random.randint(1, 9889)))) + ' 16wdtt1213'


if __name__ == "__main__":
    useragent_service.run(host='localhost', port=5001)
