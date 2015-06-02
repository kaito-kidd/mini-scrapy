# coding: utf8

""" Engine """

from gevent import monkey
monkey.patch_all()

import logging

import gevent
from gevent.pool import Pool

from scheduler import Scheduler
from downloader import Downloader
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
        all_routines = []
        all_routines.append(spawn(self._init_start_requests))
        all_routines.append(spawn(self._next_request, spider))
        join_all(all_routines)

    def _init_start_requests(self):
        """init start requests
        """
        for req in self.start_requests:
            self.crawl(req)

    def _next_request(self, spider):
        """next request
        """
        while 1:
            request = self.scheduler.next_request()
            if not request:
                gevent.sleep(0.2)
                continue
            self.pool.spawn(
                self._process_request, request, spider)

    def _process_request(self, request, spider):
        """process request
        """
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
        self.handle_spider_output(ret, spider)

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
