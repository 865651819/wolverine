import os
import redis
from pyexcel_xlsx import get_data

r = redis.StrictRedis(host='localhost', port=6379)


def import_pc_ua():
    data = get_data(os.path.join(os.getcwd(), 'bootstrap/ua-pc.xlsx'))

    start_index = 1
    end_index = 0
    for row in data["Sheet3"]:
        count = float(row[1]) * 10000
        end_index = int(start_index) + int(count)

        # store it to redis server
        for i in range(start_index, end_index):
            r.set('ua:pc:' + str(i), row[0])

        # update start_index
        start_index = end_index

    print(str(end_index) + 'entries stored')


def import_wap_ua():
    data = get_data(os.path.join(os.getcwd(), 'bootstrap/ua-wap.xlsx'))

    start_index = 1
    end_index = 0
    for row in data["Sheet2"]:
        count = int(row[1])
        end_index = start_index + count

        # store it to redis server
        for i in range(start_index, end_index):
            r.set('ua:wap:' + str(i), row[0])

        # update start_index
        start_index = end_index

    print(str(end_index) + 'entries stored')


if __name__ == '__main__':
    import_pc_ua()
