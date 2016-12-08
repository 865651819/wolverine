import urllib2
import cookielib
import requests
from bs4 import BeautifulSoup

def paw1_go(urls, user_agent, protocol, proxy_ip, proxy_port):

    # declare a CookieJar object to store cookie
    cookie = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookie)
    # Proxy Configuration
    proxy_handler = urllib2.ProxyHandler({protocol: proxy_ip + ':' + proxy_port})

    opener = urllib2.build_opener(cookie_handler, proxy_handler)

    opener.addheaders = [('User-Agent', user_agent)]

    response = opener.open(urls[0])
    soup = BeautifulSoup(response, "lxml")
    print soup.prettify()
    iframes = []
    for iframe in soup('iframe'):
        print soup.iframe.extract()


def paw_go(urls, user_agent, protocol, proxy_ip, proxy_port):

    # Proxy Configuration
    proxies = {
        protocol: proxy_ip + ':' + proxy_port
    }

    # User-Agent
    headers = {'User-Agent': user_agent}

    response = requests.get(urls[0], proxies=proxies, headers=headers)

    print response.status_code

    soup = BeautifulSoup(response.content, "lxml")
    print soup.prettify()
    iframes = []
    for iframe in soup('iframe'):
        print soup.iframe.extract()

def paw_init(url):
    pass


def paw(url, user_agent, protocol, proxy_ip, proxy_port, referer):
    # add user_agent info
    # req.add_header("User-Agent", user_agent)
    # add referer info
    # if referer:
    #    req.add_header("Referer", referer)
    pass


if __name__ == "__main__":
    paw_go(["http://www.93959.com/"],
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
           "http",
           "119.254.92.52",
           "80")
