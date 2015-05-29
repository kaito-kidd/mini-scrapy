# coding: utf8

""" TestSpider """


from http.request import Request
from spider import Spider


class TestSpider(Spider):

    """ TestSpider """

    start_urls = [
        "http://movie.douban.com/chart",
        "http://movie.douban.com/tag/",
        "http://www.douban.com/tag/%E7%88%B1%E6%83%85/?focus=movie",
        "http://www.douban.com/tag/%E5%96%9C%E5%89%A7/?focus=movie",
        "http://www.douban.com/tag/%E7%A7%91%E5%B9%BB/?focus=movie",
        "http://www.douban.com/tag/%E5%89%A7%E6%83%85/?focus=movie",
        "http://www.douban.com/tag/%E7%8A%AF%E7%BD%AA/?focus=movie",
    ]

    def parse(self, response):

        yield {"url": response.url, "status": response.status}
        yield Request("http://movie.douban.com/review/best/",
                      callback=self.parse_best)

    def parse_best(self, response):
        print response.url

    def process_item(self, item):
        print item


def main():
    spider = TestSpider()
    spider.start()


if __name__ == "__main__":
    main()
