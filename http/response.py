# coding: utf8

""" Response Object """


class Response(object):

    """ Response """

    def __init__(self, url, status=200, headers=None, body='', request=None):
        self.url = url
        self.status = status
        self.headers = headers or {}
        self.body = body
        self.request = request

    def copy(self, *args, **kwargs):
        """ copy """
        for key in ["url", "status", "headers", "body", "request"]:
            kwargs.setdefault(key, getattr(self, key))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    def __str__(self):
        return "<%d %s>" % (self.status, self.url)

    __repr__ = __str__
