import schedule
import threading
from task_queue import pv, click


def pv_job(count):
    for i in range(0, count):
        pv.apply_async()


def click_job(count):
    click.apply_async()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()






