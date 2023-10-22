import scrapy
from ..items import BroadwayItem
from ..items import OffBroadItem

class BroadwayreviewSpider(scrapy.Spider):
    name = "broadwayreview"
    allowed_domains = ["www.newyorktheatreguide.com"]
    start_urls = ["https://www.newyorktheatreguide.com/reviews/broadway"]

    def parse(self, response):
        reviews = response.css('article.jss67')
        for review in reviews:
            relative_url = review.css('h3 a ::attr(href)').get()
            review_url = 'https://www.newyorktheatreguide.com/' + relative_url
            yield response.follow(review_url, callback = self.parse_page)

        next_page = response.css('a[aria-label="Go to next page"]::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.newyorktheatreguide.com/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_page(self, response):
        broadway_review = BroadwayItem()
        
        broadway_review['show_title'] = response.css('section.jss76 p em ::text').get(),
        broadway_review['article_title'] = response.css('h1.jss57 ::text').get(),
        broadway_review['rating'] = response.css('span.MuiRating-root.jss83.jss86.MuiRating-readOnly::attr(aria-label)').get(),
        broadway_review['rating_sent'] = response.css('span.MuiRating-root.jss83.jss86.MuiRating-readOnly::attr(aria-label)').get(),
        broadway_review['body'] = response.xpath('//*[@class="jss76"]//p//text()').getall(),

        yield broadway_review
        

class OffBroadwayreviewSpider(scrapy.Spider):
    name = "offbroadwayreview"
    allowed_domains = ["www.newyorktheatreguide.com"]
    start_urls = ["https://www.newyorktheatreguide.com/reviews/off-broadway"]

    def parse(self, response):
        reviews = response.css('article.jss67')
        for review in reviews:
            relative_url = review.css('h3 a ::attr(href)').get()
            review_url = 'https://www.newyorktheatreguide.com/' + relative_url
            yield response.follow(review_url, callback = self.parse_page)

        next_page = response.css('a[aria-label="Go to next page"]::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.newyorktheatreguide.com/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_page(self, response):
        offbroad_review = OffBroadItem()

        offbroad_review['show_title'] = response.css('section.jss76 p em ::text').get(),
        offbroad_review['article_title'] = response.css('h1.jss57 ::text').get(),
        offbroad_review['rating'] = response.css('span.MuiRating-root.jss83.jss86.MuiRating-readOnly::attr(aria-label)').get(),
        offbroad_review['rating_sent'] = response.css('span.MuiRating-root.jss83.jss86.MuiRating-readOnly::attr(aria-label)').get(),
        offbroad_review['body'] = response.xpath('//*[@class="jss76"]//p//text()').getall(),
        
        yield offbroad_review