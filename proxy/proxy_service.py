import Queue
import json

import redis
from flask import Flask

proxy_service = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379)
q = Queue.Queue()


@proxy_service.route("/proxy/<int:amount>")
def proxy(amount):
    # if queue's size is smaller than requested amount, which means we need ask vendor to get more ips
    if q.qsize() < amount:
        # @TODO: use api provided by vendor
        # new_proxies = urllib2.open('')
        new_proxies = ['localhost1', 'localhost2']

        # Reuse new proxies for 5 times
        reuse = 10
        while reuse > 0:
            reuse -= 1
            for new_proxy in new_proxies:
                q.put(new_proxy)

    proxies = []
    while amount > 0:
        proxies.append(q.get())
        amount -= 1
    return json.dumps(proxies)


if __name__ == "__main__":
    proxy_service.run(host='localhost', port=5002)
