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

#filtrado nombres
nombre_carros_directo = tree.xpath('//span[@class="main-title"]/text()')
nombre_carros_directo = np.array(nombre_carros_directo)

#filtrado precios carros
precio_carros_directo = tree.xpath('//span[@class="price__fraction"]/text()')
precio_carros= np.zeros(len(precio_carros_directo))

for i in range (len(precio_carros)):
    precio_carros[i]=precio_carros_directo[i].replace('.','')
