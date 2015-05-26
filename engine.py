# coding: utf8

""" Engine """

import logging

from gevent.pool import Pool

from scheduler import Scheduler
from downloader import Downloader
from reactor import CallOnce
from utils import spawn, join_all, result2list
from http.request import Request


class Engine(object):

    """ Engine """

    def __init__(self, spider):
        self.spider = spider
        self.scheduler = Scheduler()
        self.downloader = Downloader(spider)
        self.settings = spider.settings
        max_request_size = self.settings["MAX_REQUEST_SIZE"]
        self.pool = Pool(size=max_request_size)

    def start(self):
        """start
        """
        start_requests = iter(self.spider.start_requests())
        self.execute(self.spider, start_requests)

    def execute(self, spider, start_requests):
        """execute
        """
        self.start_requests = start_requests
        self.nextcall = CallOnce(self._next_request, spider)
        join_all([spawn(self.nextcall.schedule)])

    def _next_request(self, spider):
        """_next_request
        """
        while 1:
            greenlet = self.pool.spawn(
                self._get_and_process_request, spider)
            if not greenlet.value:
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

        # 处理下载后的数据
        self.process_response(response, request, spider)

    def process_response(self, response, request, spider):
        """process response
        """
        callback = request.callback or spider.parse
        result = callback(response)
        ret = result2list(result)
        return self.handle_spider_output(ret, spider)

    def handle_spider_output(self, result, spider):
        """handle spider output
        """
        for item in result:
            if item is None:
                continue
            elif isinstance(item, Request):
                self.crawl(item)
            elif isinstance(item, dict):
                self.process_item(item, spider)
            else:
                logging.error("Spider must retrun Request, dict or None")

    def process_item(self, item, spider):
        """handle item
        """
        spider.process_item(item)

    def crawl(self, request):
        """crawl
        """
        self.scheduler.enqueue_request(request)
        self.nextcall.schedule()
