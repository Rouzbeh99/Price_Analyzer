import requests
from bs4 import BeautifulSoup
import re

page_number = 1
numberOfpages = 1
for i in range(numberOfpages):
    page = requests.get(
        'https://bama.ir/car/all-brands/all-models/all-trims?page=' + str(page_number))
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('span', attrs={'class': 'photo'})
    for link in links:
        temp = link.contents[1].attrs
        inner_page_address = temp['href']
        inner_page = requests.get(inner_page_address)
        inner_soup = BeautifulSoup(inner_page.text, 'html.parser')
        brand = inner_soup.find('span', attrs={'itemprop': 'brand'}).contents[0]
        model = inner_soup.find('span', attrs={'itemprop': 'model'}).contents[0]
        price = inner_soup.find('span', attrs={'itemprop': 'price'}).contents[0]
        price = re.sub(',', '', price)
        distance = 0
        all_infoes = inner_soup.findAll('span')
        for infoe in all_infoes:
            if len(infoe.contents) > 0 and 'کیلومتر' in infoe.contents[0] and not 'لیتر' in infoe.contents[0]:
                temp = infoe.contents[0]
                temp = re.sub("\s+", '', temp)
                temp = re.sub(',', '', temp)
                temp = re.sub('[\u0600-\u06FF]', '', temp)
                try:
                    distance = int(temp)
                except:
                    distance = 0

        print("brand = %s       model = %s        distance = %s       price = %s" % (brand, model, distance, price))
