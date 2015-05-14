# coding: utf8

""" Engine """

from scheduler import Scheduler
from downloader import Downloader


class Engine(object):

    """ Engine """

    def __init__(self, spider):
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.spider = spider
        self.settings = spider.settings

    def start(self):
        """ start """
        start_requests = iter(self.spider.start_requests())
        self.execute(self.spider, start_requests)

    def execute(self, spider, start_requests):
        """ execute """
        pass
