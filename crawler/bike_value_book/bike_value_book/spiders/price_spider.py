import scrapy

class PriceSpider(scrapy.Spider):
    name = "price"
    # start_urls = [
    #     #'./price-1.html'
    #     #'https://www.bicyclebluebook.com/SearchListingDetail.aspx?id=3068276&make=683&model=61546'
    #     #'https://www.bicyclebluebook.com/SearchListingDetail.aspx?id=3077484&make=672&model=92114'
    #     #'https://www.bicyclebluebook.com/SearchListing.aspx?make=683&model=61546'
    #     'https://www.bicyclebluebook.com/SearchBikes.aspx'
    # ]

    # def start_requests(self):
    #     urls = [
    #         # 'http://quotes.toscrape.com/page/1/',
    #         # 'http://quotes.toscrape.com/page/2/',
    #         'https://www.bicyclebluebook.com/SearchListingDetail.aspx?id=3061293&make=672&model=82960'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     rawMakeLinks = response.css("a::attr(href)").getall()
    #     cleanMakeLinks = filter(lambda x: "BicycleDatabase.aspx" in x, rawMakeLinks)
    #     cleanMakeLinks = map(lambda x : 'https://www.bicyclebluebook.com' + x, cleanMakeLinks)
    #     for makeLink in cleanMakeLinks:

    # def start_request(self):
    #     yield scrapy.Request(url='https://www.bicyclebluebook.com/SearchBikes.aspx', callback=self.parse_makes)

    # def parse_makes(self, response):
    start_urls=['https://www.bicyclebluebook.com/SearchBikes.aspx']
    def parse(self, response):
        rawMakeLinks = response.css("a::attr(href)").getall()
        cleanMakeLinks = filter(lambda x: "BicycleDatabase.aspx" in x, rawMakeLinks)
        cleanMakeLinks = map(lambda x: 'https://www.bicyclebluebook.com' + x, cleanMakeLinks)
        for makeLink in cleanMakeLinks:
            # yield{'makelink': makeLink}
            # print(makeLink)
            yield scrapy.Request(url=makeLink, callback=self.parse_models)

    def parse_models(self, response):
        rawModelLinks = response.css("a::attr(href)").getall()
        cleanModelLinks = filter(lambda x: "SearchListing.aspx" in x, rawModelLinks)
        cleanModelLinks = map(lambda x: 'https://www.bicyclebluebook.com' + x, cleanModelLinks)
        for modelLink in cleanModelLinks:
            print(modelLink)
            yield scrapy.Request(url=modelLink, callback=self.parse_years)
    
    def parse_years(self, response):
        rawYearLinks = response.css("a::attr(href)").getall()
        cleanYearLinks = filter(lambda x: "SearchListingDetail.aspx" in x, rawYearLinks)
        cleanYearLinks = map(lambda x: 'https://www.bicyclebluebook.com' + x, cleanYearLinks)
        for yearLink in cleanYearLinks:
            yield scrapy.Request(url=yearLink, callback=self.parse_bike)

    def parse_bike(self, response):
        #print(response)
        # print(len(cleanMakeLinks))
        # print(cleanMakeLinks)
        # rawLinks = response.css("a::attr(href)").getall()
        # cleanLinks = filter(lambda x: "SearchListingDetail" in x, rawLinks)
        # #print("RAWRAWRAWRAWRAWRAWRAW", rawLinks)
        
        # print(cleanLinks)
        # if not cleanLinks:  # detail bike price page
        #     # last
        # else:
        #     next_page = 

        prices=[]
        for price in response.css(".col-xs-6::text").getall():
            if '$' in price:
                clean = price.strip().replace('\r\n', '').replace(' ', '').replace('\'', '')
                prices.append(clean)
                yield{
                    'price': clean
                }
        res = {}
        for i in range(len(prices)):
            if i < len(prices)-1:
                minPrice = prices[i].split('-')[0].replace('$', '')
                maxPrice = prices[i].split('-')[1].replace('$', '')
                #minPrice = int(minPrice)
                #maxPrice = int(maxPrice)
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
                #price = int(price)
                res['msrp'] = (price)
        print(res)

