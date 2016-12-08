import random
import redis
from flask import Flask

useragent_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)


@useragent_service.route('/useragent')
def user_agent():
    key = 'ua:pc:' + str(random.seed())
    return r.get(key)
