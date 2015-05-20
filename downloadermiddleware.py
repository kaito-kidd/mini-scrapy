# coding: utf8

"""Dowloader Midlleware"""

from collections import defaultdict

from utils import iter_children_classes, call_func

from http.request import Request


class DownloaderMiddleware(object):

    """ DownloaderMiddleware iterface """

    pass


class DownloaderMiddlewareManager(object):

    """ DownloaderMiddlewareManager """

    def __init__(self, spider):
        self.settings = spider.settings
        self.methods = defaultdict(list)
        self.middlewares = self.load_middleware()
        for miw in self.middlewares:
            self._add_middleware(miw)

    def load_middleware(self):
        """load middleware
        """
        middlewares = []
        for miw in iter_children_classes(
                globals().values(), DownloaderMiddleware):
            middlewares.append(miw(self.settings))

    def _add_middleware(self, miw):
        """add middleware
        """
        if hasattr(miw, "process_request"):
            self.methods["process_request"].append(miw.process_request)
        if hasattr(miw, "process_response"):
            self.methods["process_response"].insert(0, miw.process_response)
        if hasattr(miw, "process_exception"):
            self.methods["process_exception"].insert(0, miw.process_exception)

    def download(self, download_func, request):
        """download
        """
        def process_request(request):
            """ process request """
            for method in self.methods["process_request"]:
                method(request)
            download_func(request)

        def process_response(response):
            """ process response """
            for method in self.methods["process_response"]:
                response = method(request)
                if isinstance(response, Request):
                    return response
            return response

        def process_exception(exception):
            """ process exception """
            for method in self.methods["process_exception"]:
                response = method(request, exception)
                if response:
                    return response
            return exception

        return call_func(process_request, process_exception,
                         process_response, request)


class RetryMiddleware(DownloaderMiddleware):

    """ Retry Middleware """

    RETRY_EXCEPTIONS = ()

    def __init__(self, settings):
        self.max_retry_count = settings.get_int("RETRY_COUNT")
        self.retry_status_codes = settings.get_list("RETRY_STATUS_CODES")

    def process_response(self, request, respoonse):
        """process respoonse
        """
        if request.meta.get("dont_retry", False):
            return respoonse
        if respoonse.status in self.retry_status_codes:
            return self._retry(request) or respoonse
        return respoonse

    def process_exception(self, request, exception):
        """process exception
        """
        if isinstance(exception, self.RETRY_EXCEPTIONS) \
                and request.meta.get("dont_retry", False):
            return self._retry(request)

    def _retry(self, request):
        """retry
        """
        retry_count = request.meta.get("retry_count", 0) + 1
        if retry_count <= self.max_retry_count:
            retry_request = request.copy()
            retry_request.meta["retry_count"] = retry_count
            return retry_request
