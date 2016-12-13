import os

PV_PATH = os.path.join(os.getcwd(), 'js/view.js')
PV_CLICK_PATH = os.path.join(os.getcwd(), 'js/click.js')
COOKIES_PATH = '/etc/nightmare'


def construct_args(ip, port, user_agent):
    print ' '.join(['--proxy=%s' % (str(ip) + ':' + str(port)),
                    '--user-agent="%s"' % user_agent,
                    '--ignore-ssl-errors=true'])
    return ' '.join(['--proxy=%s' % (str(ip) + ':' + str(port)),
                     '--ua="%s"' % user_agent,
                     '--ignore-ssl-errors=true'])


# '--web-security=false'
# '--load-images=false',
# '--cookies-file=%s' % (COOKIES_PATH + cookie_fn + '.txt'),


def construct_pv_cmd(urls, ip, port, user_agent):
    return 'casperjs' + ' ' + PV_PATH + ' ' + ' '.join(urls) + ' ' + construct_args(ip, port, user_agent)


def construct_pv_and_click_cmd(urls, ip, port, user_agent):
    return 'casperjs' + ' ' + PV_CLICK_PATH + ' ' + ' '.join(urls) + ' ' + construct_args(ip, port, user_agent)


if __name__ == '__main__':
    urls = ['http://www.leixp.com/jingdianqingshu/18263.html',
            'http://www.leixp.com/jingdianqingshu/18264.html',
            'http://www.leixp.com/jingdianqingshu/18265.html',
            'http://www.leixp.com/jingdianqingshu/18266.html']
    cmd = construct_pv_cmd(urls, '101.11.11.11', 90,
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    print cmd
