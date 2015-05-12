# coding: utf8

""" Request Object """


class Request(object):

    """ Request """

    def __init__(self, url, method="GET", callback=None, headers=None):
        self.url = url
        self.method = method
        self.callback = callback
        self.headers = headers or {}

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__
