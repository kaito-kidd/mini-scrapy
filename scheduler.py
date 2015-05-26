# coding: utf8

""" Scheduler """

from gevent.queue import Queue


class Scheduler(object):

    """ Scheduler """

    def __init__(self):
        self.queue = Queue()

    def enqueue_request(self, request):
        """put request
        """
        self.queue.put(request)

    def next_request(self):
        """next request
        """
        if self.queue.empty():
            return None
        return self.queue.get()

    def __len__(self):
        return self.queue.qsize()
