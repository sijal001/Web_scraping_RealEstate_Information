# -*- coding: utf-8 -*-
"""
This program is scrapying the data from the website: https://immo.vlan.be/en
Four main url link has been used to make the scraping data easier.

Certain changes has been done in the setting.py file 
1. DOWNLOAD_DELAY = 5               ----- This help delay the program by 5 seconds.
2. FEED_EXPORT_ENCODING = 'utf-8'   ----- This help scraped data be in UTF-O standard encording this makes scraped data clean and easy to understand.
3. HTTPCACHE_ENABLED = True         ----- This will not hit the server for requests already done tests will run much faster and the website will save resources.
"""

import scrapy
from time import sleep

class InformationSpider(scrapy.Spider):
    """
    This is the initial phase of the program. URL link to work with are stated here. 
    This is generated automatically when runing Scrapy command at the very beginning.
    Example base on this senario:
    
    scrapy startproject scrap_realestate
    scrapy genspider information immo.vlan.be
    """

    name = 'information'
    allowed_domains = ['immo.vlan.be']  # In most cases an extra '/' is add at the very end. We need to remove that extra '/'.
    
    # change the request_header to be oon safe side from robot.txt
    def start_requests(self):
        """
        This is the method where we state what are the links that program needs to follow at very beginning.
        Four main url link has been used to make the scraping data easier and collect some data that make sense at very beginning.
        """

        sale_house = "https://immo.vlan.be/en/real-estate/house/for-sale?propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion&countries=belgium&noindex=1"
        rent_house = "https://immo.vlan.be/en/real-estate/house/for-rent?propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion&countries=belgium&noindex=1"
        sale_apartment = "https://immo.vlan.be/en/real-estate/flat/for-sale?propertysubtypes=flat---apartment,ground-floor,penthouse,duplex,flat---studio,loft,triplex&countries=belgium&noindex=1"
        rent_apartment = "https://immo.vlan.be/en/real-estate/flat/for-rent?propertysubtypes=flat---apartment,ground-floor,penthouse,duplex,flat---studio,loft,triplex&countries=belgium&noindex=1"

        url_lst = [sale_house, rent_house, sale_apartment, rent_apartment]
        
        # Working with the for loop and statically filling the required data before hand
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
      
    def parse(self, response):
        type_of_property = response.request.meta["property_type"]
        type_of_sale = response.request.meta["sale_type"]
        
        for path in response.xpath("//div[@class='col-lg-7']/h2/a"):
            property_subtype = path.xpath(".//text()").get()
            property_subtype = (property_subtype.split())[0]
            link = path.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_collect,  meta={'property_subtype': property_subtype, 'property_type': type_of_property, 'sale_type': type_of_sale}, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"})

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
        
        # Information regarding property price 
        price = str(response.xpath("//span[@class='price']/text()").get())
        try:
            price = price[2:]
        except:
            price = price

        
        def filter_search_info(collapse, search):
            """
            Function to filter the scraping data. search specific word and filter regarding the search.
            """
            try:
                left = []
                right = []
                for num in [6,8]:
                    try:
                        title_info = response.xpath("//div[@id='{}']/div/div[@class='col-{}']/text()".format(collapse, num)).getall()
                        num_2 = 6 if num ==6 else 4
                        title_data = response.xpath("//div[@id='{}']/div/div[@class='col-{} text-right']/text()".format(collapse, num_2)).getall()
                        data_gathered = None

                        for i in title_info:
                            left.append(i.strip())

                        for i in title_data:
                            right.append(i.strip())
                        
                    except:
                        pass    
            except:
                data_gathered = None
            
            if search in left:
                for info_match, data_match in zip(left,right):
                    data_gathered = data_match
                
            else:
                data_gathered = None

            return data_gathered
        
        def yes_no(result):
            """
            Generate the Yes/No information. After scraping the data.
            """
            if result == None or result == "No":
                info = "No"
            else:
                info = "Yes"
            
            return info
    
        # Information regarding Number of facades
        kitchen_equipment = filter_search_info('collapse_kitchenbath_details', "Kitchen equipment")
        kitchen_equipment = yes_no(kitchen_equipment)

        # Furnished details 
        furnished = filter_search_info('collapse_indoor_details', "Furnished")
        furnished = yes_no(furnished)

        # Terrace data inforamtion
        terrace = filter_search_info('collapse_outdoor_details', "Terrace")
        terrace = yes_no(terrace)

        # Terrace Size
        terrace_size = filter_search_info('collapse_outdoor_details', "Surface terrace")    

        # Garden data inforamtion
        garden = filter_search_info('collapse_outdoor_details', "Garden")
        garden = yes_no(garden)

        # Garden Size
        garden_size = filter_search_info('collapse_outdoor_details', "Surface garden")

        # Information regarding Number of facades
        facades = filter_search_info('collapse_outdoor_details', "Number of facades")

        # Information regarding the swimming pool
        swimming_pool = filter_search_info('collapse_outdoor_details', "Swimming pool")
        swimming_pool = yes_no(swimming_pool)
        
        # Information regarding the build year
        build_year = filter_search_info('collapse_general_info', "Build Year")

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
            "Number of facades": facades,
            "Swimming pool": swimming_pool,
            "State of the building": build_year 
        }