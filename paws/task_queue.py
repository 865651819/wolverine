import datetime

from celery import Celery
from celery.utils.log import get_task_logger

import runner

logger = get_task_logger(__name__)

app = Celery('wolverine', broker='redis://localhost')


@app.task(name='page view')
def pv(pv_task):
    logger.info('new pv task')
    runner.pv()
    cmd = runner.construct_pv_cmd(urls=pv_task.urls, ip=pv_task.ip, port=pv_task.port, user_agent=pv_task.useragent)
    runner.run(cmd)


@app.task(name='page view with ads click')
def click(click_task):
    logger.info('new click task')
    runner.pv_click()
    cmd = runner.construct_pv_cmd(urls=click_task.url, ip=click_task.ip, port=click_task.port, user_agent=click_task.useragent)
    runner.run(cmd)


@app.task
def scratch():
    logger.info('new click task' + datetime.datetime.now())


if __name__ == '__main__':
    app.start()
