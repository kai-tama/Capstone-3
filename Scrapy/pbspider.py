import scrapy

class PbspiderSpider(scrapy.Spider):
    name = "pbspider"
    allowed_domains = ["www.playbill.com"]
    start_urls = ["https://www.playbill.com/grosses"]

    def parse(self, response):
        dropdown = response.css('div.bsp-form-select select')
        options = dropdown.xpath('//option')

        for option in options:
            option_value = option.xpath('@value').extract_first()
            yield response.follow(option_value, callback=self.parse_response)

    def parse_response(self, response):
        table = response.css('div.bsp-table-wrapper div table tbody')
        for row in table.xpath('tr'):
            yield {
                'year' : response.url[38:42],
                'show_title': row.xpath('.//td[@class="col-0"]/a/span[@class="data-value"]/text()').get(),
                'week_gross': row.xpath('.//td[@class="col-1"]/span[@class="data-value"]/text()').get(),
                'avg_ticket': row.xpath('.//td[@class="col-3"]/span[@class="data-value"]/text()').get(),
                'top_ticket': row.xpath('.//td[@class="col-3"]/span[@class="subtext"]/text()').get(),
                'seats_sold': row.xpath('.//td[@class="col-4"]/span[@class="data-value"]/text()').get(),
                'seats_in_theater': row.xpath('.//td[@class="col-4"]/span[@class="subtext"]/text()').get(),
                'num_performances': row.xpath('.//td[@class="col-5"]/span[@class="data-value"]/text()').get(),
                'capacity_filled': row.xpath('.//td[@class="col-6"]/span[@class="data-value"]/text()').get(),
            }
