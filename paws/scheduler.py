from celery import Celery
import datetime

app = Celery('wolverine', broker='redis://localhost')


@app.task
def pv():
    print 'new pv task' + datetime.datetime.now()
    pass


@app.task
def click():
    print 'new click task' + datetime.datetime.now()
    pass
