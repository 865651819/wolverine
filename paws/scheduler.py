import datetime
import json
import math
import urllib2
from random import randint

import redis
import schedule

import settings
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


def urls_group(amount):
    group = []
    while amount > 0:
        urls = [settings.SITE_HOME_PAGE]

        novel_id = randint(1, 52)
        chapter_start = randint(1, 70)
        limit = randint(10, 30)

        counter = 0

        # A hidden condition here is limit + start <= 100
        while counter < limit:
            urls.append(settings.SITE_URL.format(str(novel_id), str(chapter_start + counter)))
        group.append(urls)
    return group


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

    # Get user agent candidates
    print settings.USERAGENT_SERVICE_URL + str(jobs_to_create)
    ua_candidates = json.load(urllib2.urlopen(settings.USERAGENT_SERVICE_URL + str(jobs_to_create)))

    # Get proxy candidates
    proxy_candidates = json.load(urllib2.urlopen(settings.PROXY_SERVICE_URL + str(jobs_to_create)))

    # Get url candidates
    group = []
    amount = jobs_to_create
    while amount > 0:
        urls = [settings.SITE_HOME_PAGE]

        novel_id = randint(1, 52)
        chapter_start = randint(1, 70)
        limit = randint(10, 30)

        counter = 0

        # A hidden condition here is limit + start <= 100
        while counter < limit:
            urls.append(settings.SITE_URL.format(str(novel_id), str(chapter_start + counter)))
            counter += 1
        group.append(urls)
        amount -= 1

    # Generate concrete tasks
    for i in range(1, jobs_to_create):
        if i % 5 == 0:
            '''
            click.apply_sync((
                settings.SITE_HOME_PAGE,
                proxy_candidates[i - 1],
                proxy_candidates[i - 1],
                ua_candidates[i - 1])
            )
            '''
        else:
            pv.apply_async((group[i - 1],
                           proxy_candidates[i - 1],
                           proxy_candidates[i - 1],
                           ua_candidates[i - 1]))


schedule.every(1).seconds.do(jobs_per_sec)

while 1:
    schedule.run_pending()



