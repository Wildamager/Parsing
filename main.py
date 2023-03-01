import requests
from bs4 import BeautifulSoup
from creater import *
import textwrap as tw
import re

def get_soup(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_categories():
    url = 'https://idrone.ru'
    soup = get_soup(url)
    menu = soup.find('ul', class_ = 'ty-menu__items cm-responsive-menu')
    links = menu.find_all('a', class_ = 'ty-menu__item-link')
    for i in links:
        if i.get('href') != None:
            category = i.text.strip()
            link = url + i.get('href')
            create_categories(category, link)
    # main()


def get_products_info(products, value):
    for product in products:
        name = product.find('div', class_ = 'ty-grid-list__item-name').text.strip()
        price = product.find('div', class_ = 'ty-grid-list__price').text.strip().replace('\n', '/').split('/////')
        element_with_link_image = product.find('div', class_ = 'ty-grid-list__image')
        link = element_with_link_image.find('a', attrs={'href': re.compile("^https://")}).get('href')
        image = element_with_link_image.find('img').get('src')
        if len(price)==2:
            create_products(value, link, image, name, price[1])
        else:
            create_products(value, link, image, name, price[0])


def get_products():
    for key, value in data.items():
        soup = get_soup(value['link'])
        products_list = soup.find('div', class_ = 'ty-mainbox-body')
        products = products_list.find_all('div', class_ = 'ty-column4')
        get_products_info(products, value)
    main()

            

get_categories()
get_products()