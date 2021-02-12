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
    page = 5
    url_name = 'https://bina.az/alqi-satqi?page='
    start_urls = [
        url_name + str(page)
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
    def parse(self, response):
        item_links = response.css('.slider_controls::attr(href)').extract()
        for item_link in item_links: 
            yield response.follow(item_link, callback = self.parse_house)
        self.page += 1
        if self.page < 6:
            next_url = self.url_name + str(self.page)
            yield scrapy.Request(next_url, callback=self.parse)
        
    def parse_house(self, response):

        items = BinaItem()
        items['id'] = int(re.findall(r'\d+', response.css('.item_id::text')[0].extract())[0])
        #print('////////////////////////////////////////\n' + re.findall(r'\d+', response.css('.item_id::text')[0].extract())[0]) + '\n')
        items['title'] = response.css('.services-container>h1::text').get()
        items['price_azn'] = int(''.join(re.findall(r'\d+', response.css('.azn .price-val::text').extract()[0])))
        
        print(items['id'])

        parameters_selection = response.css('.parameters')
        
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
            else:
                if(key == 'Mərtəbə'):
                    items['n_floors'] = None
                    items['current_floor'] = None
                else:
                    items[parameters_conversion[key]] = None
        yield items

        
