import numpy as np
from lxml import html
import requests
import matplotlib.pyplot as plt


page = requests.get('https://carros.tucarro.com.co/_Desde_51')
tree = html.fromstring(page.content)

#cars quantity
quantity_from_internet = tree.xpath('//div[@class="quantity-results"]/text()')
quantity = quantity_from_internet[0].replace('resultados','')
quantity = quantity.replace(' ','')
quantity = quantity.replace('.','')
quantity = float(quantity)
quantity = quantity%50

#ejemplo en html para scraping
#<div title="buyer-name">Carson Busses</div>
#<span class="item-price">$29.95</span>

#examples
#This will create a list of buyers:
buyer = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')


#filter of car year and km
year_and_kilometres_from_internet = tree.xpath('//div[@class="item__attrs"]/text()')
year_and_kilometres = np.zeros(len(year_and_kilometres_from_internet))
years= np.zeros(len(year_and_kilometres_from_internet))
kilometres= np.zeros(len(year_and_kilometres_from_internet))

for i in range(len(year_and_kilometres_from_internet)):
    year_km=year_and_kilometres_from_internet[i]
    year_km= year_km.replace('|','')
    year_km= year_km.replace('km','')
    year_km= year_km.split('  ')
    year= year_km[0]
    year= year.replace(' ','')
    years[i]=year
    km= year_km[1]
    km= km.replace(' ','')
    kilometres[i]=km


#filter of car location
location = tree.xpath('//div[@class="item__location"]/text()')

#filter of car names
car_name_from_internet = tree.xpath('//span[@class="main-title"]/text()')
car_name = np.array(car_name_from_internet)

#filter of car prices
car_price_from_internet = tree.xpath('//span[@class="price__fraction"]/text()')
car_price= np.zeros(len(car_price_from_internet))

for i in range (len(car_price_from_internet)):
    car_price[i]=car_price_from_internet[i].replace('.','')
