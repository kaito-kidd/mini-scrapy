# coding: utf8

""" Response Object """


class Response(object):

    """ Response """

    def __init__(self, url, status=200, headers=None, request=None):
        self.url = url
        self.status = status
        self.headers = headers or {}
        self.request = request

    def __str__(self):
        return "<%d %s>" % (self.status, self.url)

    __repr__ = __str__
