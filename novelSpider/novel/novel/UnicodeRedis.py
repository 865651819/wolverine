import redis


class UnicodeRedis(redis.Redis):
    def __init__(self, *args, **kwargs):
        if "encoding" in kwargs:
            self.encoding = kwargs["encoding"]
        else:
            self.encoding = "utf-8"
        super(UnicodeRedis, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        result = super(UnicodeRedis, self).get(*args, **kwargs)
        if isinstance(result, str):
            return result.decode(encoding)
        else:
            return result
