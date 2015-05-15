# coding: utf8

""" reactory """

import gevent


class CallOnce(object):

    """ CallOnce """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.call = None

    def schedule(self):
        """schedule
        """
        if self.call is None:
            self.call = gevent.spawn(self)
            gevent.joinall([self.call])

    def __call__(self):
        self.call = None
        return self.func(*self.args, **self.kwargs)
