import requests
from bs4 import BeautifulSoup

page_number = 1
numberOfpages = 1
for i in range(numberOfpages):
    page = requests.get(
        'https://bama.ir/car/all-brands/all-models/all-trims?page=' + str(page_number))
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('span', attrs={'class': 'photo'})
    for link in links:
        temp = link.contents[1]
        inner_page_address = temp.attrs
        print(inner_page_address['href'])
