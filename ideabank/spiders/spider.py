import scrapy

from scrapy.loader import ItemLoader
from ..items import IdeabankItem
from itemloaders.processors import TakeFirst


class IdeabankSpider(scrapy.Spider):
	name = 'ideabank'
	start_urls = ['https://www.ideabank.pl/']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class, "card card")]')
		for post in post_links:
			url = post.xpath('.//h3/a/@href').get()
			date = post.xpath('.//p[@class="date"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="container"]//text()[normalize-space() and not(ancestor::h1 | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=IdeabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
