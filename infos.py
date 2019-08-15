import requests
import mysql.connector
from bs4 import BeautifulSoup
import re

connection = mysql.connector.connect(user='Rouzbeh', password='2650236000_',
                                     host='127.0.0.1',
                                     database='test')
curser = connection.cursor()
curser.execute(
    'CREATE TABLE IF NOT EXISTS Cars(Brand varchar(30) not null ,Model varchar(30) not null ,Price integer not null ,Distance integer not null )')

page_number = 0
numberOfpages = 2
for i in range(numberOfpages):
    # page_number += 1
    page = requests.get(
        'https://bama.ir/car/all-brands/all-models/all-trims?page=' + str(page_number))
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('span', attrs={'class': 'photo'})
    page_number += 1
    for link in links:
        temp = link.contents[1].attrs
        inner_page_address = temp['href']
        inner_page = requests.get(inner_page_address)
        inner_soup = BeautifulSoup(inner_page.text, 'html.parser')
        price = inner_soup.find('span', attrs={'itemprop': 'price'}).contents[0]
        price = re.sub(',', '', price)
        try:
            price = int(price)
        except:
            continue
        brand = inner_soup.find('span', attrs={'itemprop': 'brand'}).contents[0]
        model = inner_soup.find('span', attrs={'itemprop': 'model'}).contents[0]
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
                    break
                except:
                    distance = 0
                    break

        # query = 'INSERT IGNORE INTO CARS VALUE('
        # query += '\''+brand+'\''
        # query += ','
        # query += '\''+model+'\''
        # query += ','
        # query += str(price)
        # query += ','
        # query += str(distance)
        # query += ');'
        query = 'INSERT  INTO CARS (Brand,Model,Price,Distance) SELECT * FROM ( SELECT '
        query += '\'' + brand + '\''
        query += ','
        query += '\'' + model + '\''
        query += ','
        query += str(price)
        query += ','
        query += str(distance)
        query += ') AS temp WHERE NOT EXISTS ( SELECT Brand,Model,Price,Distance FROM Cars WHERE Brand ='
        query += '\'' + brand + '\' AND Model='
        query += '\'' + model + '\' AND Price='
        query += str(price) + ' AND Distance='
        query += str(distance)
        query += ');'

        print("car with brand = %s       model = %s        distance = %d       price = %d added to database" % (
            brand, model, distance, price))

        curser.execute(query)

connection.commit()
