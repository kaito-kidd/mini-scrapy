# coding: utf8

""" Downloader """

import requests


class DownloaderHandler(object):

    """ DownloaderHandler """

    def __init__(self):
        self.session = requests.Session()

    def fetch_request(self, url):
        self.session.get(url)


class Downloader(object):

    """ Downloader """

    def __init__(self):
        pass

    def fetch(self, request, spider):
        """fetch

        @request, Request, 请求
        """
        pass
