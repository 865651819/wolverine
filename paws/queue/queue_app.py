from celery import Celery
from paws.actions import paw_view, paw_click

queue_app = Celery('wolverine', broker='redis://localhost')


@queue_app.task
def paw_view(urls):
    print 'paw view'
    paw_view(urls)


@queue_app.task
def paw_click(url):
    print 'paw_click'
    paw_click(url)
