import requests


def paw_go(urls, user_agent, protocol, proxy_ip, proxy_port):
    # Proxy Configuration
    proxies = {
        protocol: proxy_ip + ':' + proxy_port
    }

    # User-Agent
    headers = {'User-Agent': user_agent}

    response = requests.get(urls[0], proxies=proxies, headers=headers)

    print response.status_code


if __name__ == "__main__":
    paw_go(["http://www.93959.com/"],
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
           "http",
           "119.254.92.52",
           "80")
