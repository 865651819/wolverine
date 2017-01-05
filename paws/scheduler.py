import schedule
import json
import redis
import settings
import datetime
import math
import urllib2

from task_queue import pv, click

r = redis.StrictRedis(host='localhost', port=6379)

ACCESS_PCT = [
    4.23,
    3.06,
    1.67,
    1.18,
    1.13,
    0.9,
    2.23,
    3.15,
    4.13,
    4.83,
    5.33,
    5.66,
    5.95,
    5.90,
    5.44,
    5.22,
    5.17,
    5.72,
    5.26,
    5.48,
    5.86,
    5.32,
    5.45,
    4.6]


def jobs_per_sec():
    print 'pv_jobs_per_sec'

    # Get current hour of the day
    hour = datetime.datetime.today().hour

    # Get target for current day
    jobs_to_create = 0
    try:
        jobs_to_create = int(math.ceil((r.get(settings.TASKS_TOTAL) * (ACCESS_PCT[hour] / 100)) / 3600))
    except:
        jobs_to_create = 10

    print '[Paw] ' + str(jobs_to_create) + ' jobs to start...'

    ua_candiates = json.loads(urllib2.urlopen(url=settings.PROXY_SERVICE_URL + str(jobs_to_create)))

    for i in range(0, jobs_to_create):
        pv.apply_async()


schedule.every(1).seconds.do(jobs_per_sec)

while 1:
    schedule.run_pending()



