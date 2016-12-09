import requests
import json
from random import randint
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


PROXY_URL = 'http://localhost:5002/next_proxy'
USER_AGENT_URL = 'http://localhost:5001/useragent'


def paw_views(urls):
    # http://stackoverflow.com/questions/17082425/running-selenium-webdriver-with-a-proxy-in-python
    # Download geckodriver and put it under /use/bin
    fp = webdriver.FirefoxProfile()

    # build proxy
    proxy_response = json.loads(requests.get(PROXY_URL).content)['_values']
    fp.set_preference('network.proxy.type', 1)
    # fp.set_preference('network.proxy.http', encode(proxy_response['ipAddress']))
    # fp.set_preference('network.proxy.http_port', int(encode(proxy_response['port'])))
    fp.set_preference('network.proxy.http', '113.225.41.106')
    fp.set_preference('network.proxy.http_port', 8118)

    # User Agent
    fp.set_preference('general.useragent.override', encode(requests.get(USER_AGENT_URL).content))

    fp.update_preferences()
    driver = webdriver.Firefox(firefox_profile=fp)

    proxy_referer = None

    # Visit first page
    try:
        for url in urls:
            print url
            sec = randint(2, 10)
            print sec
            driver.implicitly_wait(sec)
            driver.get(url)
    finally:
        driver.close()


def encode(string):
    return string.encode('ascii', 'ignore')


if __name__ == "__main__":
    # paw_go(["http://www.93959.com/"],
    #        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    #        "http",
    #        "119.254.92.52",
    #        "80")
    paw_views(['http://www.leixp.com/jingdianqingshu/18263.html',
               'http://www.leixp.com/jingdianqingshu/18264.html',
               'http://www.leixp.com/jingdianqingshu/18265.html',
               'http://www.leixp.com/jingdianqingshu/18266.html'])
