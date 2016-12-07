import random

import redis

r = redis.StrictRedis(host='localhost', port=6379)


def get_pc_ua(seed):
    key = 'ua:pc:' + str(seed)
    return r.get(key)


def get_wap_ua(seed):
    key = 'ua:wap:' + str(seed)
    return r.get(key)


def get_next_pc_ua():
    # hard coded entry
    random.seed()
    return get_pc_ua(random.randint(1, 9889))


def get_next_wap_ua():
    random.seed()
    return get_wap_ua(random.randint(1, 8732))
