import schedule
import threading
from task_queue import pv, click


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



