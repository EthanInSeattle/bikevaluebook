import scrapy
import re

class PriceSpider(scrapy.Spider):
    # name of the spider, used when invoking the spider through command line
    name = "price"

    # starting point of the spider, use self.parse as callback by default
    start_urls=['https://www.bicyclebluebook.com/SearchBikes.aspx']

    # extract links of all makes
    def parse(self, response):
        rawMakeLinks = response.css("a::attr(href)").getall()
        cleanMakeLinks = filter(lambda x: "BicycleDatabase.aspx" in x, rawMakeLinks)
        cleanMakeLinks = map(lambda x: 'https://www.bicyclebluebook.com' + x, cleanMakeLinks)
        for makeLink in cleanMakeLinks:
            yield scrapy.Request(url=makeLink, callback=self.parse_models)

    # extract links of all models
    def parse_models(self, response):
        rawModelLinks = response.css("a::attr(href)").getall()
        cleanModelLinks = filter(lambda x: "SearchListing.aspx" in x, rawModelLinks)
        cleanModelLinks = map(lambda x: 'https://www.bicyclebluebook.com' + x, cleanModelLinks)
        for modelLink in cleanModelLinks:
            yield scrapy.Request(url=modelLink, callback=self.parse_years)
    
    # extract year, make, model, category, and link of all years
    def parse_years(self, response):
        rawContent = response.css(".values-line").getall()
        for content in rawContent:
            #make = content.css(".col-sm-2").get()
            year = re.search(r'<div class="col-sm-1 col-xs-1">(.*?)</div>', content).group(1)
            make = re.search(r'<div class="col-sm-2 col-xs-3">(.*?)</div>', content).group(1)
            model = re.search(r'<div class="col-sm-3 col-xs-3">(.*?)</div>', content).group(1)
            category = re.search(r'<div class="col-sm-2 col-xs-2 truncate">(.*?)</div>', content).group(1)
            link = 'https://www.bicyclebluebook.com' + re.search(r'onclick="location.href=\'(.*?)">', content).group(1)
            yield scrapy.Request(url=link, callback=self.parse_bike, cb_kwargs={'year':year, 'make':make, 'model':model, 'category':category})

    # extract bike price evaluation and description
    def parse_bike(self, response, year, make, model, category):
        prices=[]
        for price in response.css(".col-xs-6::text").getall():
            if '$' in price:
                clean = price.strip().replace('\r\n', '').replace(' ', '').replace('\'', '')
                prices.append(clean)
        res = {'year':year, 'make':make, 'model':model, 'category':category}
        for i in range(len(prices)):
            if i < len(prices)-1:
                minPrice = prices[i].split('-')[0].replace('$', '')
                maxPrice = prices[i].split('-')[1].replace('$', '')
                if i == 0:
                    res["excellent"] = (minPrice, maxPrice)
                elif i == 1:
                    res["very-good"] = (minPrice,maxPrice)
                elif i == 2:
                    res['good'] = (minPrice, maxPrice)
                elif i == 3:
                    res['fair'] = (minPrice, maxPrice)
            else:
                price = prices[i].replace(',', '').replace('$', '')
                res['msrp'] = (price)
        res['img'] = response.css('.col-sm-12 img::attr(src)').get()
        res['raw-description'] =  response.css(".bvg-product-details").get()
        yield res
