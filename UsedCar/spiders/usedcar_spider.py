from UsedCar.items import used_car_item
import scrapy

class usedcar_spider(scrapy.Spider):
    name = 'usedcar'
    allowed_urls = ['https://newyork.craigslist.org/']
    #get all the start page for each specific year
    pages=[]
    for i in range(1997,2018):
        pages.append('https://newyork.craigslist.org/search/cto?max_auto_year=%(year)d&min_auto_year=%(year)d&sort=date&s=0' %
                 {'year':i})
    start_urls = pages
    #for each year, get all the pages of post, and build a loop to go through all the pages
    def parse(self, response):
        try:
            total_num = response.xpath('//span[@class="button pagenum"]/span[@class="totalcount"]/text()').extract()
            #total_num[0] is the number of cars
            page_nums = int(total_num[0])
        except:
            page_nums = 0
        #get the auto_year_model
        try:
            auto_year = response.xpath('//div[@class="minmax auto_year"]/input[@name="min_auto_year"]/@value').extract()
        except:
            auto_year = ['NA']
        #get all the pages for this specific year
        pageurls=[]
        try:
            for i in range(page_nums//120):
                pageurls.append('https://newyork.craigslist.org/search/cto?max_auto_year=%(year)s&min_auto_year=%(year)s&sort=date&s=%(num)d' %
                    {'year':auto_year[0], 'num':i*120})
        except:
            pageurls=['']

        for pageurl in pageurls:
            yield scrapy.Request(pageurl, callback=self.parse_page)

    #parse each page contains 120 cars at most. get some items, and recall lower level parse for each car
    def parse_page(self, response):

        url_list = response.xpath('//div[@id="sortable-results"]/ul/li/a/@href').extract()
        year_model = response.xpath('//div[@class="minmax auto_year"]/input[@name="min_auto_year"]/@value').extract()
        if year_model == []:
            year_model = ['NA']
        if url_list == []:
            url_length = -1
        else:
            url_length = len(url_list)
        #for loop length of url_list, get price, date and url for a specific post
        for i in range(url_length):
                #extract the ith li. the tags of price, date, url
            price = response.xpath('(//div[@id="sortable-results"]/ul/li)[%d]/p/span/span[@class="result-price"]/text()' % (i+1)).extract()
            date = response.xpath('(//div[@id="sortable-results"]//li)[%d]/p/time/@datetime' % (i+1)).extract()
            url = response.xpath('(//div[@id="sortable-results"]/ul/li)[%d]/a/@href' % (i+1)).extract()
            title = response.xpath('(//div[@id="sortable-results"]/ul/li)[%d]/p/a/text()' % (i+1)).extract()
            notice = response.xpath('(//div[@id="sortable-results"]/ul/li)[%d]/p/span/span[@class="result-hood"]/text()' % (i+1)).extract()
            #get wheather the post has pic ('Y') or not ('N')
            pic_label = response.xpath('(//div[@id="sortable-results"]/ul/li)[%d]/p/span/span[@class="result-tags"]/text()' % (i+1)).extract()
            map_label = response.xpath('(//div[@id="sortable-results"]/ul/li)[%d]/p/span/span[@class="result-tags"]/span[@class="maptag"]/text()' % (i+1)).extract()
            try:
                if (pic_label[0]).strip().find('pic')!=-1:
                    has_pic = ['Y']
            except:
                has_pic = ['N']
            try:
                if map_label != []:
                    has_map = ['Y']
            except:
                has_map = ['N']

            if price == []:
                price = ['NA']
            if date == []:
                date = ['NA']
            if title == []:
                title = ['NA']
            try:
                if notice == []:
                    notice = ['NA']
            except:
                pass

            yield scrapy.Request(url[0], callback=self.parse_car, meta={'date':date,
                'price':price,'title':title,'notice':notice,'has_map':has_pic,'has_pic':has_pic,'year_model':year_model})

    #parse each car
    def parse_car(self, response):
        item = used_car_item()
        item['date'] = response.meta['date']
        item['price'] = response.meta['price']
        item['title'] = response.meta['title']
        item['notice'] = response.meta['notice']
        item['has_pic'] = response.meta['has_pic']
        item['has_map'] = response.meta['has_map']
        item['year_model'] = response.meta['year_model']
        #get the title, if not, empty
        try:
            item['model'] = response.xpath('(//div[@class="mapAndAttrs"]/p[@class="attrgroup"])[1]/span/b/text()').extract()
            
        except:
            item['model'] = ['NA']
        #get the pic link
        item['pic_link'] = response.xpath('//div[@class="gallery"]//div[@class="swipe-wrap"]/div/img/@src').extract()
        if item['pic_link'] == []:
            item['pic_link']=['NA']

        #get the map detail
        item['latitude'] = response.xpath('//div[@id="map"]/@data-latitude').extract()            
        if item['latitude'] == []:
            item['latitude'] = ['NA']
        item['longitude'] = response.xpath('//div[@id="map"]/@data-longitude').extract()
        if item['longitude'] == []:
            item['longitude'] = ['NA']
        item['location'] = response.xpath('//div[@class="mapbox"]/div[@class="mapaddress"]/text()').extract()
        if item['location'] == []:
            item['location'] = ['NA']


        #get the atributs list
        try:    
            attr = response.xpath('(//div[@class="mapAndAttrs"]/p)[2]//text()').extract()
            attr = [x for x in [y.strip() for y in attr] if x!='']
        except:
            attr = ['','']

        #get the atributes dictionary
        dic={} 
        for i in range(0, len(attr), 2):
            dic.update({attr[i]:attr[i+1]})
        #obtain values, in different forms, else empty string
        try:
            item['VIN'] = dic['VIN:']
        except:
            item['VIN'] = ['NA']

        #obtain values, in different forms, else empty string
        try:
            item['cylinders'] = dic['cylinders:']
        except:
            try:
                item['cylinders']=dic['cylinder:']
            except:
                item['cylinders']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['drive'] = dic['drive:']
        except:
            try:
                item['drive']=dic['drive']
            except:
                item['drive']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['fuel'] = dic['fuel:']
        except:
            try:
                item['fuel']=dic['fuel']
            except:
                item['fuel']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['odometer'] = dic['odometer:']
        except:
            try:
                item['odometer']=dic['odometer']
            except:
                item['odometer']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['title_status'] = dic['title status:']
        except:
            try:
                item['title_status']=dic['title status']
            except:
                item['title_status']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['transmission'] = dic['transmission:']
        except:
            try:
                item['transmission']=dic['transmission']
            except:
                item['transmission']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['body_type'] = dic['type:']
        except:
            try:
                item['body_type']=dic['type']
            except:
                item['body_type']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['ex_color'] = dic['paint color:']
        except:
            try:
                item['ex_color']=dic['color:']
            except:
                item['ex_color']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['condition'] = dic['condition:']
        except:
            item['condition']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['size'] = dic['size:']
        except:
            item['size']=['NA']
        #obtain values, in different forms, else empty string
        try:
            item['in_color'] = dic['inside color']
        except:
            item['in_color']=['NA']

        yield item

