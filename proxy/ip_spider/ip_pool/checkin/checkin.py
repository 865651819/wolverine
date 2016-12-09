import redis
import json
import datetime


def save(ip_items, source):
    r = redis.StrictRedis(host='localhost', port=6379)

    counter = 0
    for ip_item in ip_items:
        counter += 1
        ip_json = json.dumps(ip_item.__dict__)
        r.set('proxy:' + str(counter), ip_json)

    # Record summary
    summary = {
        'source': source,
        'count': len(ip_items)
    }
    r.set('lastUpdated:' + str(datetime.datetime.utcnow()), str(summary))
