# coding: utf8

""" 工具 """

import inspect
import logging
import urllib
import hashlib

from urlparse import urlparse, parse_qsl, urlunparse

import gevent


def get_logger(name):
    """创建一个logger
    """
    default_logger = logging.getLogger(name)
    default_logger.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
    stream.setFormatter(formatter)
    default_logger.addHandler(stream)
    return default_logger

logger = get_logger("mylogger")


def call_func(func, errback=None, callback=None, *args, **kwargs):
    """执行某个函数,并自动包装异常和回调

    @func, function, 待执行的函数
    @errback, func, 异常回调
    @callback, func, 最终回调
    @args, tuple, 参数
    @kwargs, dict, 名字参数
    """
    try:
        result = func(*args, **kwargs)
    except Exception as exc:
        if errback:
            errback(exc)
    else:
        if callback:
            result = callback(result)
        return result


def spawn(func, *args, **kwargs):
    """ spawn
    """
    return gevent.spawn(func, *args, **kwargs)


def join_all(funcs):
    """join all
    """
    gevent.joinall(funcs)


def iter_children_classes(values, clazz):
    """iter children classes
    """
    for obj in values:
        if inspect.isclass(obj) and issubclass(obj, clazz) \
                and obj is not clazz:
            yield obj


def result2list(result):
    """result to list
    """
    if result is None:
        return []
    if isinstance(result, (dict, basestring)):
        return [result]
    if hasattr(result, "__iter__"):
        return result


def request_fingerprint(request):
    """request fingerprint
    """
    scheme, netloc, path, params, query, fragment = urlparse(request.url)
    keyvals = parse_qsl(query)
    keyvals.sort()
    query = urllib.urlencode(keyvals)
    canonicalize_url = urlunparse((
        scheme, netloc.lower(), path, params, query, fragment))
    fpr = hashlib.sha1()
    fpr.update(canonicalize_url)
    return fpr.hexdigest()
