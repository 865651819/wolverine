import redis
import json
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


def merge():
    keys = r.keys('novel:[^:]')
    print keys

    res = []
    for key in keys:
        print key
        val = r.get(key)
        val = val.replace("'", '"').replace('\\\\', '\\')
        print val
        #val = unicode(val)
        print 'dumped!'
        val = json.dumps(val)
        #print val
        o = json.loads(val)
        print o
        res.append(str(o))
        print res
    print res

    r.set('novels', res)



if __name__ == "__main__":
    merge()
