# coding: utf8

""" Downloader """

from urlparse import urlparse

import requests

from http.response import Response
from downloadermiddleware import DownloaderMiddlewareManager
from utils import logger


class DownloadHandler(object):

    """ DownloadHandler """

    def __init__(self, spider, keep_alive=True, **kwargs):
        self.keep_alive = keep_alive
        self.settings = spider.settings
        self.session_map = {}
        self.kwargs = kwargs

    def _get_session(self, url):
        """get session

        @url, str, url
        """
        netloc = urlparse(url).netloc
        if self.keep_alive:
            if url not in self.session_map:
                self.session_map[netloc] = requests.Session()
            return self.session_map[netloc]
        return requests.Session()

    def fetch(self, request):
        """fetch
        """
        proxy = request.meta.get("proxy")
        kwargs = {
            "headers": request.headers,
            "timeout": self.settings["TIMEOUT"],
        }
        if proxy:
            kwargs["proxies"] = {"http:": proxy}
            logger.info("user proxy %s", proxy)
        kwargs.update(self.kwargs)
        url = request.url
        session = self._get_session(url)
        logger.info("processing %s", url)
        response = session.get(url, **kwargs)
        return Response(response.url, response.status_code,
                        response.headers, response.content)


class Downloader(object):

    """ Downloader """

    def __init__(self, spider):
        self.hanlder = DownloadHandler(spider)
        self.middleware = DownloaderMiddlewareManager(spider)

    def fetch(self, request, spider):
        """fetch

        @request, Request, 请求
        """
        return self.middleware.download(self._download, request)

    def _download(self, request):
        """download
        """
        return self.hanlder.fetch(request)
