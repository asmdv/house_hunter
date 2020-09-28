import scrapy
from ..items import BinaItem
import re
class BinaSpyder(scrapy.Spider):
    
    # Get parameters in parameters tabel in house page view of Bina.az
    # returns dictionary of parameters
    def get_parameters(self, parameters):
        dict = {}
        for i in range(len(parameters.css('tr'))):
            dict[parameters.css('tr')[i].css('td::text')[0].extract()] = parameters.css('tr')[i].css('td::text')[1].extract()
        return dict

    name = 'bina'
    start_urls = [
            'https://bina.az/items/1709244'
    ]


#    def parse(self, response):
#        items = BinaItem() 
#        quotes = response.css('.quote')
#        for quote in quotes:
#            items['text'] = quote.css('.text::text').extract()[0]
#            items['author'] = quote.css('.author::text').extract()[0]
#            yield items
#
#        next = response.css('li.next a::attr(href)').get()
#        if next is not None:
#            yield response.follow(next, callback = self.parse)
#    def parse(self, response):
#        yield self.parse_house(response)
        
    def parse_house(self, response):

        items = BinaItem()
        items['id'] = int(re.findall(r'\d+', response.css('.item_id::text')[0].extract())[0])
        print(items['id'])
        items['price_azn'] = int(''.join(re.findall(r'\d+', response.css('.azn .price-val::text').extract()[0])))
        
        #Take parameters table in the apartment page
        parameters_selection = response.css('.parameters')
        parameters_dict = self.get_parameters(parameters_selection)  
        parameters_conversion = {'Kateqoriya': 'category', 'Mərtəbə': 'floor', 'Otaq sayı': 'n_rooms', 'Kupça': 'deed_of_sale' }

        for key, value in parameters_conversion.items():
            if key in parameters_dict.keys():

                if key == 'Mərtəbə':
                    floors_digits = re.findall(r'\d+', parameters_dict[key])
                    items['n_floors'] = int(floors_digits[1]) 
                    items['current_floor'] = int(floors_digits[0]) 
                elif key == 'Otaq sayı':
                    items[parameters_conversion[key]] = int(parameters_dict[key])
                elif key == 'Kupça':
                    items[parameters_conversion[key]] = True if parameters_dict['Kupça'] == 'var' else False
                else:
                    items[parameters_conversion[key]] = parameters_dict[key]
        yield items

        
