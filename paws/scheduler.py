import schedule
import threading
import datetime
from task_queue import pv, click

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


def pv_jobs_per_sec():
    print 'pv_jobs_per_sec'
    jobs_to_create = 20
    for i in range(0, jobs_to_create):
        pv.apply_async()


def click_job(count):
    click.apply_async()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(1).seconds.do(pv_jobs_per_sec)

while 1:
    schedule.run_pending()



