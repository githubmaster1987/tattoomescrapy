# -*- coding: utf-8 -*-
import scrapy
from tattoomescraper.items import TattoomescraperItem
import re
from scrapy.http import Request

class TattoomespiderSpider(scrapy.Spider):
    name = "tattoomespider"
    allowed_domains = ["tattoome.com"]
    start_urls = (
        'https://www.tattoome.com/fr/loc/2/france/',
        #'https://www.tattoome.com/fr/org/2528/misti-ka-custom-tattoo-shop',
    )

    index = 1
    error_cnt = 0
    home_url = ""

    def parse(self, response):
    #def parse_temp(self, response):
        container_div = response.xpath('//div[@class="container-fluid"]')

        if self.error_cnt == 3:
            print "Exit"
            return

        if self.home_url == "":
            self.home_url = "https://www.tattoome.com/fr/loc/2/france"

        if response.url == "https://www.tattoome.com/fr/loc/2/france" and self.index > 1:
            self.error_cnt = self.error_cnt + 1
        else:
            urls = []
            ids = []
            for row in container_div:
                header_div = row.xpath('div[@class="row resultat_header"]')

                div_a = header_div.xpath('div/h3/a')
                a_href = div_a.xpath('@href').extract()
                a_text = div_a.xpath('text()').extract()
                if len(a_href) == 1:
                    url = response.urljoin(a_href[0])
                    title = a_text[0]
                    id = a_href[0].split("/")[3]
                    req = Request(url=url, callback=self.parse_detail)
                    req.meta['page_url'] = self.home_url
                    # yield Request(url=url, callback=self.parse_detail)
                    yield req

        self.index = self.index + 1
        self.home_url = "https://www.tattoome.com/fr/loc/2/france/" + str(self.index)
        #print (home_url, self.error_cnt, response.url)
        yield Request(url=self.home_url, callback=self.parse, headers={"X-Requested-With":"XMLHttpRequest"}, dont_filter=True)

    def parse_detail(self, response):
        page_url = response.meta['page_url']
        item = TattoomescraperItem()
        item["tatt_page_url"] = page_url
        item["tatt_detail_url"] = response.url

        title = response.xpath('//div[@class="studio_content_width studio_content_header"]/h1/span/text()').extract()
        if len(title) > 0 :
            item["tatt_title"] = title[0]
        else:
            item["tatt_title"] = ""

        city = response.xpath('//div[@class="studio_content_width studio_content_header"]/p/text()').extract()
        if len(city) > 0:
            item["tatt_city"] = city[0]
        else:
            item["tatt_city"] = ""

        breadcrumbs = response.xpath('//ol[@class="breadcrumb"]/li')
        breadcrumb = []
        first_bread = response.xpath('//ol[@class="breadcrumb"]/li/span/a/text()').extract()
        breadcrumb.append(first_bread)

        for it in breadcrumbs:
            str = it.xpath('a/span/text()').extract()
            if len(str) > 0:
                breadcrumb.append(str)

        item["tatt_breadcrumbs"] = breadcrumb

        person_names = response.xpath('//div[@class="studio_tatoueurs"]/ul[@class="nav nav-tabs"]/li[@role="presentation"]/a/text()').extract()
        item["tatt_person_name"] = person_names

        phone_number_in = response.xpath('//p[@class="well well-sm phone-number collapse in"]/text()').extract()
        phone_number_out = response.xpath('//p[@class="well well-sm collapse phone-number"]/text()').extract()

        phone_number = ""
        if len(phone_number_in) > 0:
            phone_number = phone_number_in[0]

        if len(phone_number_out) > 0:
            phone_number = phone_number_out[0]

        item["tatt_phone_number"] = phone_number

        address = response.xpath('//div[@class="studio_localisation_adresse"]/p/text()').extract()

        if len(address) > 0:
            item["tatt_address"] = address
        else:
            item["tatt_address"] = ""

        scripts = response.xpath('//script/text()').extract()
        for script in scripts:
            values = re.search(r'google.maps.LatLng\((.*?)\);', script, re.M|re.I|re.S)
            if values is not None:
                item["tatt_coordinate"] = values.group(1)

        styles = response.xpath('//span[@class="resultat_content_texte_tag"]/text()').extract()
        item["tatt_style"] = styles

        item["tatt_id"] = response.url.split("/")[5]

        images = response.xpath('//a[@href="#x"]/img/@src').extract()
        item["tatt_picture"] = images
        yield item
