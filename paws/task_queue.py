from celery import Celery
from celery.utils.log import get_task_logger
import datetime
import runner


logger = get_task_logger(__name__)

app = Celery('wolverine', broker='redis://localhost')


@app.task(name='page view')
def pv():
    logger.info('new pv task' + datetime.datetime.now())
    runner.pv()


@app.task(name='page view with ads click')
def click():
    logger.info('new click task' + datetime.datetime.now())
    runner.pv_click()


@app.task
def scratch():
    logger.info('new click task' + datetime.datetime.now())


if __name__ == '__main__':
    app.start()
