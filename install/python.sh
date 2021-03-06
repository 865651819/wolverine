#!/usr/bin/env bash
pip install redis

# install html parser lxml
brew install libxml2

# install pyexcel_xlsx
pip install pyexcel_xlsx

# install beautifulsoup4
pip install beautifulsoup4

# install parser html5lib
pip install html5lib

pip install requests

pip install flask

pip install Celery

pip install pyvirtualdisplay

pip install chronos-python

pip install schedule


cd wolverine
celery -A paws worker --app=paws.task_queue --loglevel=info

pip install pymongo