# coding: utf8

""" TestSpider """


from http.request import Request
from spider import Spider


class TestSpider(Spider):

    """ TestSpider """

    start_urls = [
        "http://movie.douban.com/chart",
        "http://movie.douban.com/tag/",
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
