import os
from multiprocessing import Pool

PV_PATH = os.path.join(os.getcwd(), 'js/view.js')
PV_CLICK_PATH = os.path.join(os.getcwd(), 'js/click.js')
COOKIES_PATH = '/etc/nightmare'

CNT = 0;


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


def pv():
    global CNT
    CNT += 1
    print CNT


def pv_click():
    global CNT
    CNT += 1
    print CNT


if __name__ == '__main__':
    # start 100 worker processes
    pool = Pool(processes=100)


