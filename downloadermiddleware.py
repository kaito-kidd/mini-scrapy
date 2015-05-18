# coding: utf8

"""Dowloader Midlleware"""

from collections import defaultdict


class DownloaderMiddleware(object):

    """ DownloaderMiddleware iterface """

    pass

class DownloaderMiddlewareManager(object):

    """ DownloaderMiddlewareManager """

    def __init__(self, spider):
        self.settings = spider.settings
        self.methods = defaultdict(list)
        self.middlewares = self.load_middleware()
        for mw in self.middlewares:
            self._add_middleware(mw)

    def load_middleware(self):
        """load middleware
        """
        middlewares = []
        for mw in iter_classes(globals().values(), DownloaderMiddleware):
            middlewares.append(mw(self.settings))

    def _add_middleware(self, mw):
        """add middleware
        """
        if hasattr(mw, "process_request"):
            self.methods["process_request"].append(mw.process_request)
        if hasattr(mw, "process_response"):
            self.methods["process_response"].insert(0, mw.process_response)
        if hasattr(mw, "process_exception"):
            self.methods["process_exception"].insert(0, mw.process_exception)

    def download(self, request):
        """download
        """
        pass


class RetryMiddleware(DownloaderMiddleware):

    """ Retry Middleware """

    RETRY_EXCEPTIONS = ()

    def __init__(self, settings):
        self.max_retry_count = settings.get_int("RETRY_COUNT")
        self.retry_status_codes = settings.get_list("RETRY_STATUS_CODES")

    def process_response(self, request, respoonse):
        """process respoonse"""
        if request.meta.get("dont_retry", False):
            return respoonse
        if respoonse.status in self.retry_status_codes:
            return self._retry(request, respoonse) or respoonse
        return respoonse

    def process_exception(self, request, exception):
        """process exception"""
        if isinstance(exception, RETRY_EXCEPTIONS) \
                and request.meta.get("dont_retry", False):
            return self._retry(request, respoonse)

    def _retry(self, request, respoonse):
        """retry
        """
        retry_count = request.meta.get("retry_count", 0) + 1
        if retry_count <= self.max_retry_count:
            retry_request = request.copy()
            retry_request.meta["retry_count"] = retry_count
            return retry_request
