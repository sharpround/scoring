import scrapy

# king arthur flour (apparently) uses https://schema.org/Recipe

class KingArthurFlourSpider(scrapy.Spider):
    name = 'kingarthurflour'
    start_urls = ['http://www.kingarthurflour.com/recipes/bread/no-knead?page=all']

    def parse(self, response):
        links = response.css('a[id="rec_URL_1A"]::attr(href)') + response.css('a[id="rec_URL_2A"]::attr(href)')

        for href in links:
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('h1[itemprop="name"]::text').extract()[0]
            # 'votes': response.css('.question .vote-count-post::text').extract()[0],
            # 'body': response.css('.question .post-text').extract()[0],
            # 'tags': response.css('.question .post-tag::text').extract(),
            # 'link': response.url,
        }
