from CarReview.items import CarReviewItem
import scrapy

class car_review_spider(scrapy.Spider):
    name = 'carreview'
    allowed_urls = ['https://www.carsguide.com.au']
    #get all the start page for each specific year
    start_urls = ['https://www.carsguide.com.au/mlp/makes']

    def parse(self,response):
        makers_link = response.xpath('//div[@class="makes-logo"]//li/a/@href').extract()
        urls_list = ['https://www.carsguide.com.au'+ i for i in makers_link]
        makers = [i[1:] for i in makers_link]
        for i in range(len(urls_list)):
            maker = makers[i]
            yield scrapy.Request(urls_list[i], callback=self.parse_maker, meta={'maker':maker})


    def parse_maker(self,response):
        maker = response.meta['maker']
        models_link = response.xpath('//div[@class="cg-model-model clearfix"]//div[@class="view-content"]/div[@class="item-list"]//li/a/@href').extract()
        urls_list = ['https://www.carsguide.com.au'+ i for i in models_link]
        try:
            models = [i.split('/')[2] for i in models_link]
        except:
            models = list(range(len(models_link)))
        for i in range(len(models_link)):
            model=models[i]
            yield scrapy.Request(urls_list[i], callback=self.parse_review, meta={'maker':maker,'model':model})

    def parse_review(self,response):
        maker = response.meta['maker']
        model = response.meta['model']
        reviews_link = response.xpath('//div[@class="node node-review view-mode-cg_summary clearfix noHoverBg"]/div/a/@href').extract()
        urls_list = ['https://www.carsguide.com.au'+ i for i in reviews_link]
        try:
            for url in urls_list:
                yield scrapy.Request(url, callback=self.parse_final, meta={'maker':maker,'model':model, 'link':url})
        except:
            pass

    def parse_final(self, response):
        item = CarReviewItem()
        item['maker'] = response.meta['maker']
        item['model'] = response.meta['model']
        item['link'] = response.meta['link']
        item['score'] = response.xpath('//div[@class="reviewTotalScore reviewReset"]/div[@class="reviewTotalScore--score"]/span/text()').extract()
        item['pros'] = response.xpath('//div[@class="whatWeLike--sectionLike"]//li/text()').extract()
        item['cons'] = response.xpath('//div[@class="whatWeLike--sectionDont"]//li/text()').extract()
        comment = response.xpath('//div[@class="blockWrapper articleWrapper container articleWrapperFY17 "]/div/div[@class="articleBody"]//text()').extract()
        if comment==[]:
            try:
                comment = response.xpath('//div[@class="field field-name-cg-article-body"]/div/p/text()').extract()
            except:
                pass
        item['comment'] = comment
        title = response.xpath('//div[@class="field field-name-fy17-content-area field-type-ds field-label-hidden"]/div/div/div[@class="page-container container"]/h1/text()').extract()
        if title ==[]:
            try:
                title = response.xpath('//div[@class="col-lg-9 col-md-8 one-col main-col"]//div[@class="field field-name-title"]/h1/text()').extract()
            except:
                pass
        item['title'] = title
        yield item
