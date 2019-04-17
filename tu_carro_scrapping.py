import numpy as np
from lxml import html
import requests
import matplotlib.pyplot as plt


page = requests.get('https://carros.tucarro.com.co/')
tree = html.fromstring(page.content)


#ejemplo en html para scraping
#<div title="buyer-name">Carson Busses</div>
#<span class="item-price">$29.95</span>


#This will create a list of buyers:
buyer = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

#filter of car names
car_name_from_internet = tree.xpath('//span[@class="main-title"]/text()')
car_name = np.array(car_name_from_internet)

#filter of car prices
car_price_from_internet = tree.xpath('//span[@class="price__fraction"]/text()')
car_price= np.zeros(len(car_price_from_internet))

for i in range (len(car_price_from_internet)):
    car_price[i]=car_price_from_internet[i].replace('.','')
