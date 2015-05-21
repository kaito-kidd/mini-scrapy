# coding: utf8

""" Downloader """

from urlparse import urlparse

import requests

from http.response import Response
from downloadermiddleware import DownloaderMiddlewareManager


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
        if self.keep_alive:
            if url not in self.session_map:
                self.session_map[urlparse(url).netloc] = requests.Session()
            return self.session_map[url]
        return requests.Session()

    def fetch(self, url):
        """fetch
        """
        kwargs = {
            "headers": self.settings["DEFAULT_HEADERS"],
            "timeout": self.settings["TIMEOUT"]
        }
        kwargs.update(self.kwargs)
        session = self._get_session(url)
        response = session.get(url, kwargs=kwargs)
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
        self.middleware.download(self._download, request)

    def _download(self, request):
        """download
        """
        return self.hanlder.fetch(request.url)
