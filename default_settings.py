# coding: utf8

""" default config settings """

RETRY_COUNT = 3

RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 408]

TIMEOUT = 10

DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
}

PROXY_ENABLED = False

MAX_REQUEST_SIZE = 30
