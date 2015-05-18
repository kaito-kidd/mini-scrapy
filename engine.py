# coding: utf8

""" Engine """

import logging

from scheduler import Scheduler
from downloader import Downloader
from reactor import CallOnce
from utils import spawn, join_all
from http.request import Request


class Engine(object):

    """ Engine """

    def __init__(self, spider):
        self.spider = spider
        self.scheduler = Scheduler()
        self.downloader = Downloader(spider)
        self.settings = spider.settings
        self.funcs = []

    def start(self):
        """ start """
        start_requests = iter(self.spider.start_requests())
        self.execute(self.spider, start_requests)

    def execute(self, spider, start_requests):
        """ execute """
        self.start_requests = start_requests
        self.nextcall = CallOnce(self._next_request, spider)
        self.funcs.append(spawn(self.nextcall.schedule))
        join_all(self.funcs)

    def _next_request(self, spider):
        """ _next_request """
        while 1:
            if not self._get_and_process_request(spider):
                break

        if self.start_requests:
            try:
                req = next(self.start_requests)
            except StopIteration:
                self.start_requests = None
            else:
                self.crawl(req)

    def _get_and_process_request(self, spider):
        """get and process request
        """
        request = self.scheduler.next_request()
        if not request:
            return None
        try:
            response = self.download(request, spider)
        except Exception as exc:
            logging.error("download error: %s", str(exc), exc_info=True)
        else:
            self._handle_downloader_output(response, request, spider)
            return response

    def download(self, request, spider):
        """ download
        """
        response = self.downloader.fetch(request, spider)
        response.request = request
        self.nextcall.schedule()
        return response

    def _handle_downloader_output(self, response, request, spider):
        """hanlde downloader output
        """
        if isinstance(response, Request):
            self.crawl(response)
            return

    def crawl(self, request):
        """ crawl
        """
        self.scheduler.enqueue_request(request)
        self.nextcall.schedule()
