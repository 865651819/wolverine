import requests
import json
from random import randint
from selenium import webdriver
from paws import runner

PROXY_URL = 'http://localhost:5002/next_proxy'
USER_AGENT_URL = 'http://localhost:5001/useragent'


def paw_views_py(urls):
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


def paw_view_js(urls):
    # build proxy
    # proxy_response = json.loads(requests.get(PROXY_URL).content)['_values']
    proxy_el = requests.get(PROXY_URL).content.split(':')
    ip = encode(proxy_el[0])
    port = encode(proxy_el[1])

    # build user_agent
    user_agent = encode(requests.get(USER_AGENT_URL).content)
    view_cmd = runner.construct_pv_cmd(urls=urls, ip=ip, port=port, user_agent=user_agent)
    print view_cmd


def encode(string):
    return string.encode('ascii', 'ignore')


if __name__ == "__main__":
    # paw_go(["http://www.93959.com/"],
    #        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    #        "http",
    #        "119.254.92.52",
    #        "80")
    paw_view_js([
        'http://www.91txs.net/lishi/yishi/201607/11995.html',
        'http://www.91txs.net/tansuo/faming/201608/12417.html',
        'http://www.91txs.net/tansuo/faming/201607/11930.html',
        'http://www.91txs.net/ziran/qqdw/201607/12105.html',
        'http://www.91txs.net/shehui/fengsu/201507/1829.html',
        'http://www.91txs.net/shehui/quwen/201507/6527.html',
        'http://www.91txs.net/shehui/tuku/201603/11054.html'])
