import Queue
import json
import urllib2
import schedule

import redis
from flask import Flask

proxy_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)
q = Queue.Queue()


@proxy_service.route("/proxy")
def proxy():
    # if queue's size is smaller than requested amount, which means we need ask vendor to get more ips
    if q.empty():
        return []

    proxies = []
    while not q.empty():
        proxies.append(q.get())
    return json.dumps(proxies)


def fetch_new_proxies():
    new_proxies = urllib2.urlopen('http://114.55.65.167:8888/api.asp?ddbh=yh001&noinfo=true&sl=11&text=true').read().split()
    print 'Fetch new proxies'
    for new_proxy in new_proxies:
        print new_proxy
        q.put(new_proxy)

schedule.every(3).minutes.do(fetch_new_proxies)

while 1:
    schedule.run_pending()

if __name__ == "__main__":
    proxy_service.run(host='localhost', port=5002)
