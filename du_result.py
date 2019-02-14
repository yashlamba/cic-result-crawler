# -*- coding: utf-8 -*-
import scrapy

class DuResultSpider(scrapy.Spider):
    name = 'du-result'
    allowed_domains = ['duresult.in/students/Combine_GradeCard.aspx']
    start_urls = ['http://duresult.in/students/Combine_GradeCard.aspx/']

    def parse_result(self, response):
        yield {
            'NAME': response.css('span[id="lblname"] > b::text').extract()[0],
            'TOTAL_MARKS': response.xpath('//table[@id="gvrslt"]/tr/td[2]/text()').extract()[0],
            'MAX_MARKS': 850,
            'PERCENTAGE': (int(response.xpath('//table[@id="gvrslt"]/tr/td[2]/text()').extract()[0])/850)*100,
        }
        
    def parse(self, response):
        for rno in range(18312911001, 18312911045):
            data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
               '__VIEWSTATE': response.css('input[id="__VIEWSTATE"]::attr(value)').extract()[0],
                '__VIEWSTATEGENERATOR': '35D4F7A9',
                '__EVENTVALIDATION': response.css('input[id="__EVENTVALIDATION"]::attr(value)').extract()[0],
                'ddlcollege': '312',
                'txtrollno': str(rno),
                'txtcaptcha': response.css('img[id="imgCaptcha"]::attr(src)').extract()[0].split('=')[1].split('&')[0],
                'btnsearch': 'Print+Score+Card',    
            }
            yield scrapy.FormRequest(url=self.start_urls[0], formdata=data, callback=self.parse_result, dont_filter=True)

    