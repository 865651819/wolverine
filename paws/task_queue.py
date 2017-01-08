import datetime
import runner
import settings
import redis

from celery import Celery
from celery.utils.log import get_task_logger

r = redis.StrictRedis(host='localhost', port=6379)

logger = get_task_logger(__name__)

app = Celery('wolverine', broker='redis://localhost')


@app.task(name='page view')
def pv(job_id, urls, proxy, useragent):
    # print 'ip ' + proxy
    # logger.info('[' + str(job_id) + '] new pv task')
    # cnt = runner.pv()
    try:
        ip_port = proxy.split(':')
    except:
        print 'ip error'
        return
    cmd = runner.construct_pv_cmd(urls=urls, ip=ip_port[0], port=ip_port[1], user_agent=useragent)
    # print str(cnt) + ':' + cmd
    pv_cnt = int(r.get(settings.PLANNED_PV_COUNT_KEY)) + len(urls)
    r.set(settings.PLANNED_PV_COUNT_KEY, pv_cnt)
    runner.run(cmd)


@app.task(name='page view with ads click')
def paw(job_id, url, proxy, useragent):
    # print 'ip ' + proxy
    # logger.info('[' + str(job_id) + '] new click task')
    # cnt = runner.pv_click()
    try:
        ip_port = proxy.split(':')
    except:
        print 'ip error'
        return
    cmd = runner.construct_pv_and_click_cmd(url=url, ip=ip_port[0], port=ip_port[1], user_agent=useragent)
    # print str(cnt) + ':' + cmd
    pv_cnt = int(r.get(settings.PLANNED_CLICK_COUNT_KEY)) + 1
    r.set(settings.PLANNED_CLICK_COUNT_KEY, pv_cnt)
    runner.run(cmd)


@app.task
def scratch():
    logger.info('new click task' + datetime.datetime.now())


if __name__ == '__main__':
    app.start()
