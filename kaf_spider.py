import scrapy

# king arthur flour (apparently) uses https://schema.org/Recipe

class KingArthurFlourSpider(scrapy.Spider):
    name = 'kingarthurflour'
    start_urls = ['http://www.kingarthurflour.com/recipes/bread/no-knead?page=all']

    def parse(self, response):
        links = response.xpath('a[id="rec_URL_1A"]/@href') + \
        		response.xpath('a[id="rec_URL_2A"]/@href')

        for href in links:
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_recipe)

    def parse_category(self, response):
        pass

    def parse_recipe(self, response):
        yield {
            'name':             response.xpath('//*[@itemprop="name"]/text()').extract(),
            'rating':           response.xpath('//*[@itemprop="ratingValue"]/@content').extract(),
            'num_ratings':      response.xpath('//*[@itemprop="reviewCount"]/text()').extract(),
            'date':             response.xpath('//*[@itemprop="datePublished"]/@content').extract(),
            'kaf_guaranteed':   response.xpath('//*[@data-serverid="kafGuaranteed_flag"]').extract(),
            'headnotes':        response.xpath('//*[@data-serverid="HeadNotes"]/text()').extract(),
            'ingredients':      response.xpath('//*[@id="g_ingredients"]//li').extract(),
            'instructions':     response.xpath('//*[@itemprop="recipeInstructions"]/li/span/text()').extract()
            # 'author':           response.xpath('//*[@data-serverid="recipe_author"]').extract(),
            # 'prep_time':        response.xpath('//*[@itemprop="prepTime"]').extract(),
            # 'cook_time':        response.xpath('//*[@itemprop="prepTime"]').extract(),
            # 'prep_time':        response.xpath('//*[@itemprop="prepTime"]').extract(),
            }