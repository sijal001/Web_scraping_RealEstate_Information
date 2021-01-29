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
        """
        yield scrapy.Request(url=sale_house, callback=self.parse, meta={'property_type': "house", 'sale_type': "sale"},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})
        """

    def parse(self, response):
        type_of_property = response.request.meta["property_type"]
        type_of_sale = response.request.meta["sale_type"]
        
        for path in response.xpath("//div[@class='col-lg-7']/h2/a"):
            property_subtype = path.xpath(".//text()").get()
            property_subtype = (property_subtype.split())[0]
            link = path.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_collect,  meta={'property_subtype': property_subtype, 'property_type': type_of_property, 'sale_type': type_of_sale}, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})
            sleep(10)

        for i in range(2,21):
            path = f"//div[@class='pager']//ul/li[{i}]/a/@href"
            next_page = response.xpath(path).get()
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'property_type': type_of_property, 'sale_type': type_of_sale},
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})
                        
    def parse_collect(self, response):
        address = response.xpath("//span[@class='address-line  ico btn-address pl-4']/text()").get()
        post_code = response.xpath("//span[@class='city-line pl-4']/text()[1]").get()
        city = response.xpath("//span[@class='city-line pl-4']/text()[2]").get()
        type_of_property = response.request.meta["property_type"]
        property_subtype_info = response.request.meta["property_subtype"]
        type_of_sale = response.request.meta["sale_type"]
        bed_rooms = response.xpath("//div[@class='fs-4'][1]/text()").get()
        living_surface = response.xpath("//div[@title='Livable Surface']//div[3]/text()").get()
        
        # Price 
        price = response.xpath("//span[@class='price']/text()").get()
        try:
            price = price[2:]
        except:
            price = price

        # Kitchen data information
        try: 
            kitchen_equipment_info = response.xpath("//div[@id='collapse_kitchenbath_details']//div[1]//div[1]/text()").get()
            if kitchen_equipment_info == 'Kitchen equipment':
                kitchen_equipment = response.xpath("//div[@id='collapse_kitchenbath_details']//div[1]//div[2]/text()").get()
            else:
                kitchen_equipment = "No"
            
            if kitchen_equipment != "No":
                kitchen_equipment = "Yes"
        except:
            kitchen_equipment = "No"

        # Furnished data inforamtion 
        try:
            furnished_info = response.xpath("//div[@id='collapse_indoor_details']//div[3]//div[1]/text()").get()
            if furnished_info == 'Furnished':
                furnished = response.xpath("//div[@id='collapse_indoor_details']//div[3]//div[2]/text()").get()
            else:
                furnished = "No"
            
            if furnished != "No":
                furnished = "Yes"
        except:
            furnished = "No"

        # Terrace data inforamtion 
        try:
            terrace_info = response.xpath("//div[@id='collapse_outdoor_details']//div[6]//div[1]/text()").get()
            if terrace_info == 'Terrace':
                terrace = response.xpath("//div[@id='collapse_outdoor_details']//div[6]//div[2]/text()").get()
            else:
                terrace = "No"
                terrace_size = "0"
            
            if terrace != "No":
                terrace = "Yes"
                terrace_size = response.xpath("//div[@id='collapse_outdoor_details']//div[7]//div[2]/text()").get()
        except:
            terrace = "No"
            terrace_size = "0"

        # Garden data inforamtion 
        try:
            garden_info = response.xpath("//div[@title='Garden']//div[2]/text()").get()
            if garden_info == 'Garden':
                garden = "Yes"
            else:
                garden = "No"
                garden_size = "0"

            if garden != "No":
                garden = "Yes"
                garden_size = response.xpath("//div[@title='Garden']//div[3]/text()").get()
        except:
            garden = "No"
            garden_size = "0"
        
        # Number of facades data inforamtion 
        try:
            no_facades_info = response.xpath("//div[@id='collapse_outdoor_details']//div[2]//div[1]/text()").get()
            if no_facades_info == 'Number of facades':
                no_facades = response.xpath("normalize-space(//div[@id='collapse_outdoor_details']//div[2]//div[2]/text())").get()
            else:
                no_facades = "0"
   
        except:
            no_facades = "0"

        # Swiming Pool data inforamtion 
        try:
            swiming_pool_info = response.xpath("//div[@class='row section collapsable-section']//div[11]//div[1]/text()").get()
            if swiming_pool_info == 'Swimming pool':
                swiming_pool = response.xpath("//div[@id='collapse_indoor_details']//div[3]//div[2]/text()").get()
            else:
                swiming_pool = "No"
            
            if swiming_pool != "No":
                swiming_pool = "Yes"
        except:   
            swiming_pool = "No"

        
        # code to calculate the property state
        # House New or old
        search_for_year = response.xpath("normalize-space(//div[@id='collapse_general_info']/div/div[@class='col-6']/text())")
        search_for_year_date = response.xpath("normalize-space(//div[@id='collapse_general_info']/div/div[@class='col-6 text-right']/text())")
        build_year = None
        try:
            for find_match, year_match in zip(search_for_year,search_for_year_date):
                if find_match.get() == "Build Year":
                    build_year = year_match.get()
                    
        except:
            # building_state = None
            build_year = None
             
        

        yield {
            "Address": address,
            "Post Code": post_code,
            "City": city,
            "Type of property": type_of_property,
            "Property Subtype": property_subtype_info,
            "Price": price,
            "Type of sale": type_of_sale,
            "Number of rooms": bed_rooms,
            "Area": living_surface,
            "Fully equipped kitchen": kitchen_equipment,
            "Furnished": furnished,
            "Terrace":  terrace,
            "Terrace Area": terrace_size,
            "Garden": garden,
            "Garden Area":garden_size,
            "Number of facades": no_facades,
            "Swimming pool": swiming_pool,
            "State of the building": build_year 
        }