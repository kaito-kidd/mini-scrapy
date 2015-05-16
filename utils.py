# coding: utf8

import gevent

""" 工具 """

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
