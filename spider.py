# coding: utf8

""" Base Spider"""

from conf.settings import Settings
from http.request import Request
from engine import Engine


class Spider(object):

    """ Base Spider"""

    custom_settings = None

    def __init__(self):
        if not hasattr(self, "start_urls"):
            self.start_urls = []
        # init settings
        self.settings = Settings(self.custom_settings)

        self.initialize()

    def initialize(self):
        """initialize
        """
        pass

    def start_requests(self):
        """start_requests
        """
        for url in self.start_urls:
            yield Request(url)

    def start(self):
        """start
        """
        engine = Engine(self)
        engine.start()

    def parse(self, response):
        """parse
        """
        raise NotImplementedError

    def process_item(self, item):
        """process item
        """
        pass
