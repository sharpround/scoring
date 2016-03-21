import scrapy

# king arthur flour (apparently) uses https://schema.org/Recipe

class KingArthurFlourSpider(scrapy.Spider):
    name = 'kingarthurflour'
    start_urls = ['http://www.kingarthurflour.com/recipes/bread/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/breakfast-and-brunch/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/cake/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/cookies-bars-and-candy/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/entres-sides-and-appetizers/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/favorite-classics/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/frozen-treats/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/gluten-free/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/miscellaneous/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/pies-tarts-and-turnovers/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/pizza-and-flatbread/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/scones/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/sourdough/view-all?page=all',
                  'http://www.kingarthurflour.com/recipes/whole-wheat/whole-grain-/view-all?page=all']


    def parse(self, response):
        links = response.xpath('//a[@id="rec_URL_1A"]/@href') + response.xpath('//a[@id="rec_URL_2A"]/@href')

        for href in links:
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        yield {
            'url':              response.url,
            'name':             response.xpath('//*[@itemprop="name"]/text()').extract(),
            'rating':           response.xpath('//*[@itemprop="ratingValue"]/@content').extract(),
            'num_ratings':      response.xpath('//*[@itemprop="reviewCount"]/text()').extract(),
            'date':             response.xpath('//*[@itemprop="datePublished"]/@content').extract(),
            'kaf_guaranteed':   response.xpath('//*[@data-serverid="kafGuaranteed_flag"]/text()').extract(),
            'headnotes':        response.xpath('//*[@data-serverid="HeadNotes"]/text()').extract(),
            'v_ingredients':    response.xpath('//*[@id="v_ingredients"]//li').extract(),
            'w_ingredients':    response.xpath('//*[@id="w_ingredients"]//li').extract(),
            'g_ingredients':    response.xpath('//*[@id="g_ingredients"]//li').extract(),
            'instructions':     response.xpath('//*[@itemprop="recipeInstructions"]/li/span/text()').extract()
        }
            # 'author':           response.xpath('//*[@data-serverid="recipe_author"]').extract(),
            # 'prep_time':        response.xpath('//*[@itemprop="prepTime"]').extract(),
            # 'cook_time':        response.xpath('//*[@itemprop="prepTime"]').extract(),
            # 'prep_time':        response.xpath('//*[@itemprop="prepTime"]').extract(),