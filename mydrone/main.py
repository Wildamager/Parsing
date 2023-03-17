
import requests
from bs4 import BeautifulSoup
#This is file for create json-file
from creater import * 
import textwrap as tw
import re
import random
import time
from progress.bar import IncrementalBar

url = 'https://mydrone.ru/'

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
    descriptions  = soup.find('div', id = 'content_description').text
    try:
        сharacteristics = soup.find('div', class_ = 'ty-wysiwyg-content').text
    except:
        сharacteristics = None
    info = {'description':descriptions,
            'сharacteristics': сharacteristics}
    return info 

def get_info(product):
    name = product.find('a', class_ = 'product-title').text
    print(name)
    link = product.find('a', class_ = 'product-title').get('href')
    image = product.find('img').get('data-src')
    if image == None:
            image = product.find('img').get('src')
    try: 
        price = product.find('span', class_ = 'ty-price').text
    except AttributeError:
        price = None
    description = get_description(link)
    return {'name':name,
            'link':link,
            'image':image,
            'price': price,
            'info':description}

def get_pagination(link):
    soup = get_soup(link)
    try:
        if soup.find('a', class_='cm-history ty-pagination__item hidden-phone ty-pagination__range cm-ajax')!=None:
            pagination = soup.find('div', class_='ty-pagination')
            end_num = pagination.find_all('a')[-1].text.split(' ')[-1]
            print(int(end_num))
            return int(end_num)
        else:
            pagination = soup.find('div', class_='ty-pagination__items')
            print(pagination.text.replace('\n','')[-1])
            return int(pagination.text.replace('\n','')[-1])
    except:
        print(1)
        return 1
        

def get_products(link):
    products = []
    for i in range(0,get_pagination(link)):
        page = f'page-{str(i+1)}/'
        print(link+page)
        soup = get_soup(link+page)
        list_of_products = soup.find_all('div', class_ = 'ty-column3')
        
        for product in list_of_products:
            try:
                products.append(get_info(product))
            except:
                continue
        
    return products
        
    



def get_submenu_list(soup):
    submenu_list_div=soup.find_all('div', class_ = 'ty-menu__submenu-item')
    submenu_list = []
    for subcategory in submenu_list_div:
        if url in subcategory.find('a').get('href'):
            submenu_list.append({'name':subcategory.text.replace('\n', '').strip(),
                                 'link':subcategory.find('a').get('href'),
                                 'products': get_products(subcategory.find('a').get('href'))})
        else:
            submenu_list.append({'name':subcategory.text.replace('\n', '').strip(),
                                 'link': url + subcategory.find('a').get('href')[1:],
                                 'products': get_products(url + subcategory.find('a').get('href')[1:])})
    return submenu_list


def get_submenu(soup):
    submenu = soup.find_all('div', class_ = 'second-lvl')
    submenu_list=[]
    for sub in submenu:
        header = sub.find('div', class_ = 'ty-menu__submenu-item-header')
        name = header.find('bdi').text
        link = url + header.find('a', class_ = 'ty-menu__submenu-link').get('href')[1:]
        try:
            image = header.find('img').get('data-src')
        except AttributeError:
            image = None
        subcategories = sub.find('div', class_  = 'ty-menu__submenu')
        if subcategories != None:
            submenu_list.append((name, link, image, get_submenu_list(subcategories)))
        else:
            submenu_list.append((name, link, image, None, get_products(link)))
    return submenu_list
        

def get_menu():
    soup = get_soup(url)
    menu_ul = soup.find('ul', class_ = 'ty-menu__items cm-responsive-menu')
    categories_li = menu_ul.find_all('li', class_ = 'ty-menu__item cm-menu-item-responsive first-lvl')
    for category in categories_li:

        create_categories(category.find('bdi').text, get_submenu(category)) 

    main()


get_menu()