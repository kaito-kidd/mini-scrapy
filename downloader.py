# coding: utf8

""" Downloader """

from urlparse import urlparse

import requests


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
        if url not in self.session_map:
            self.session_map[urlparse(url).netloc] = requests.Session()
        return self.session_map[url]

    def fetch(self, url):
        """fetch
        """
        kwargs = {
            "headers": self.settings["DEFAULT_HEADERS"],
            "timeout": self.settings["TIMEOUT"]
        }
        kwargs.update(self.kwargs)
        session = self._get_session(url)
        respoonse = session.get(url, kwargs=kwargs)
        return respoonse


class Downloader(object):

    """ Downloader """

    def __init__(self, spider):
        self.hanlder = DownloadHandler(spider)
        self.middleware = DownloaderMiddlewareManager(spider)

    def fetch(self, request, spider):
        """fetch

        @request, Request, 请求
        """
        self.middleware.download(request)
        return self.hanlder.fetch(request.url)
