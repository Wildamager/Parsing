import requests
from bs4 import BeautifulSoup
#This is file for create json-file
from creater import * 
import textwrap as tw
import re
import random
import time
from progress.bar import IncrementalBar

def get_soup(link):
    proxies = ["http://89.179.78.113:10800",
               "http://45.130.43.221:1080",
               "http://89.232.123.2:3128",
               "http://194.38.3.242:5678",
               "http://94.253.95.241:3629"]
    header = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
	}
    response = requests.get(link, headers=header, proxies={"http":random.choice(proxies)})
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_description(link):
    soup = get_soup(link)
    description = soup.find('div',id='content_description').text
    return description

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
    print(f'Выделено {len(links)} категорий')


def get_products_info(products, value):
    bar = IncrementalBar('Download', max = len(products))
    for product in products:
        bar.next()
        time.sleep(0.1)
        name = product.find('div', class_ = 'ty-grid-list__item-name').text.strip()
        price = product.find('div', class_ = 'ty-grid-list__price').text.strip().replace('\n', '/').split('/////')
        element_with_link_image = product.find('div', class_ = 'ty-grid-list__image')
        link = element_with_link_image.find('a', attrs={'href': re.compile("^https://")}).get('href')
        image = element_with_link_image.find('img').get('data-src')
        if image == None:
            image = element_with_link_image.find('img').get('src')
        description = get_description(link)
        if len(price)==2:
            create_products(value, link, image, name, price[1], description)
        else:
            create_products(value, link, image, name, price[0], description)
    bar.finish()


def get_pagination(soup):
    pagination_number = soup.find('a', class_ = 'cm-history ty-pagination__item hidden-phone ty-pagination__range cm-ajax')
    if pagination_number != None:
        number = int(pagination_number.text.split(' ')[-1])
        return number
    else:
        pagination_list = soup.find('div', class_ = 'ty-pagination__items')
        end_of_pagination_list = int(pagination_list.find_all('a')[-1].text)
        return end_of_pagination_list



def get_products():
    for key, value in data.items():
        print('\n')
        print(key)
        soup = get_soup(value['link'])
        if value['link'] == 'https://idrone.ru/shop/?features_hash=36-7641':
            for i in range(get_pagination(soup)):
                page = f'page-{str(i+1)}/'
                print(page)
                soup = get_soup(f'https://idrone.ru/shop/{page}?features_hash=36-7641')
                products_list = soup.find('div', class_ = 'ty-mainbox-body')
                products = products_list.find_all('div', class_ = 'ty-column4')
                try:
                    get_products_info(products, value)
                except AttributeError:
                    continue
        else: 
            for i in range(get_pagination(soup)):
                page = f'page-{str(i+1)}/'
                print(page)
                soup = get_soup(value['link']+page)
                products_list = soup.find('div', class_ = 'ty-mainbox-body')
                products = products_list.find_all('div', class_ = 'ty-column4')
                try:
                    get_products_info(products, value)
                except AttributeError:
                    continue
    main()

            
#For start parsing you need runing this 2 func 
get_categories()
get_products()