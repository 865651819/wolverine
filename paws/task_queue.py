import datetime

from celery import Celery
from celery.utils.log import get_task_logger

import runner

logger = get_task_logger(__name__)

app = Celery('wolverine', broker='redis://localhost')


@app.task(name='page view')
def pv(urls, ip, port, useragent):
    logger.info('new pv task')
    cnt = runner.pv()
    cmd = runner.construct_pv_cmd(urls=urls, ip=ip, port=port, user_agent=useragent)
    print str(cnt) + ':' + cmd
    #runner.run(cmd)


@app.task(name='page view with ads click')
def paw(url, ip, port, useragent):
    logger.info('new click task')
    cnt = runner.pv_click()
    cmd = runner.construct_pv_and_click_cmd(url=url, ip=ip, port=port, user_agent=useragent)
    print str(cnt) + ':' + cmd
    #runner.run(cmd)


@app.task
def scratch():
    logger.info('new click task' + datetime.datetime.now())


if __name__ == '__main__':
    app.start()
