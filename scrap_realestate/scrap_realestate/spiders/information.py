# -*- coding: utf-8 -*-
import scrapy
from time import sleep

class InformationSpider(scrapy.Spider):
    name = 'information'
    allowed_domains = ['immo.vlan.be']

    
    # change the request_header to be oon safe side from robot.txt
    def start_requests(self):
        sale_house = "https://immo.vlan.be/en/real-estate/house/for-sale?propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion&countries=belgium&noindex=1"
        rent_house = "https://immo.vlan.be/en/real-estate/house/for-rent?propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion&countries=belgium&noindex=1"
        sale_apartment = "https://immo.vlan.be/en/real-estate/flat/for-sale?propertysubtypes=flat---apartment,ground-floor,penthouse,duplex,flat---studio,loft,triplex&countries=belgium&noindex=1"
        rent_apartment = "https://immo.vlan.be/en/real-estate/flat/for-rent?propertysubtypes=flat---apartment,ground-floor,penthouse,duplex,flat---studio,loft,triplex&countries=belgium&noindex=1"

        url_lst = [sale_house, rent_house, sale_apartment, rent_apartment]
        
        
        for link in url_lst:
            if link == sale_house:
                type_of_property = "house"
                type_of_sale = "sale"
            elif link == sale_apartment:
                type_of_property = "apartment"
                type_of_sale = "sale"
            elif link == rent_house:
                type_of_property = "house"
                type_of_sale = "rent"
            elif link == rent_apartment:
                type_of_property = "apartment"
                type_of_sale = "rent"
            yield scrapy.Request(url=link, callback=self.parse, meta={'property_type': type_of_property, 'sale_type': type_of_sale},
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})
        
        #yield scrapy.Request(url=sale_house, callback=self.parse, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})


    def parse(self, response):
        type_of_property = response.request.meta["property_type"]
        type_of_sale = response.request.meta["sale_type"]
        for path in response.xpath("//div[@class='col-lg-7']/h2/a"):
            property_subtype = path.xpath(".//text()").get()
            property_subtype = (property_subtype.split())[0]
            link = path.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_collect,  meta={'property_subtype': property_subtype, 'property_type': type_of_property, 'sale_type': type_of_sale}, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})
            
            # Each page 2 seconds
            sleep(2)
            
    def parse_collect(self, response):
        address = response.xpath("//span[@class='address-line  ico btn-address pl-4']/text()").get()
        post_code = response.xpath("//span[@class='city-line pl-4']/text()[1]").get()
        city = response.xpath("//span[@class='city-line pl-4']/text()[2]").get()
        type_of_property = response.request.meta["property_type"]
        property_subtype_info = response.request.meta["property_subtype"]
        price = response.xpath("//span[@class='price']/text()").get()
        type_of_sale = response.request.meta["sale_type"]
        bed_rooms = response.xpath("//div[@class='fs-4'][1]/text()").get()
        living_surface = response.xpath("//div[@title='Livable Surface']//div[3]/text()").get()
        
        # Kitchen data information fill
        kitchen_equipment_info = response.xpath("//div[@id='collapse_kitchenbath_details']//div[1]//div[1]/text()").get()
        if kitchen_equipment_info == 'Kitchen equipment':
            kitchen_equipment = response.xpath("//div[@id='collapse_kitchenbath_details']//div[1]//div[2]/text()").get()
        else:
            kitchen_equipment = "No"
        
        if kitchen_equipment != "No":
            kitchen_equipment = "Yes"

        
    
        yield {
            "Address": address,
            "Post Code": post_code,
            "City": city,
            "Type of property": type_of_property,
            "Property Subtype": property_subtype_info,
            "Price": price[2:],
            "Type of sale": type_of_sale,
            "Number of rooms": bed_rooms,
            "Area": living_surface,
            "Fully equipped kitchen": kitchen_equipment,
        }
        
        """
        for i in range(2,5):
            next_page = response.xpath(f"//div[@class='pager']//ul/li[{i}]/@href").get()

            yield scrapy.Request(url=next_page, callback=self.parse_collect, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})
        """