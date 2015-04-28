# coding: utf8

""" Engine """

from scheduler import Scheduler
from downloader import Downloader


class Engine(object):

    """ Engine """

    def __init__(self):
        self.scheduler = Scheduler()
        self.downloader = Downloader()
