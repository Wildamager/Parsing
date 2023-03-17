import requests
from bs4 import BeautifulSoup
#This is file for create json-file
import textwrap as tw
import re
import random
import time
from progress.bar import IncrementalBar
import json


def get_soup(link):
    proxies = ["http://89.179.78.113:10800","http://174.70.1.210:8080","http://173.201.183.110:80","http://209.97.150.167:8080",
               "http://45.130.43.221:1080","http://66.29.154.105:3128","http://134.209.29.120:3128","http://134.209.108.182:8888",
               "http://89.232.123.2:3128","http://65.20.224.102:8080","http://203.13.32.91:8080","http://185.162.228.193:8080",
               "http://194.38.3.242:5678","http://203.24.109.96:80","http://203.32.121.19:80","http://45.8.106.7:80",
               "http://94.253.95.241:3629",]
    header = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
	}
    try: 
        response = requests.get(link, headers=header)
    except:
        proxy = random.choice(proxies)
        response = requests.get(link, headers=header, proxies={"http":proxy})
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_specs(link):
    time.sleep(5)
    soup = get_soup(link)
    try:
        specs = soup.find('section', class_ = 'section-specs').text
        if specs == None:
            specs = soup.find('div', class_ = 'select-content').text
        return specs
    except AttributeError:
        return None

def get_products(soup, input):
    series_bottom_list = soup.find_all('ul', class_ = 'series-bottom-list')
    series_top_list = soup.find_all('ul', class_ = 'series-top-list')
    print(len(series_bottom_list))
    data = {}
    data[input] = []
    bar = IncrementalBar('Download', max = len(series_bottom_list))
    for index_of_top_list,seria in enumerate(series_bottom_list):
        bar.next()
        category = series_top_list[index_of_top_list].text
        for info in seria:
            series_cover = info.find('div', class_ = 'series-cover')
            links_with_info = series_cover.find_all("a")
            for product in links_with_info:
                name = product.get('data-ga-label').split('-')[-1]
                image = product.find('img').get('data-nav-lazy')
                link = product.get('href').split('?')[0] + '/specs'
                discription = get_specs(link)
                data[input].append({'name':name,
                                             'chapter':category,
                                             'description':discription,
                                             'pages':[image],
                                             'url':link,
                                             'site':input
                                            })
    bar.finish()
    return data

def main(input):
    soup = get_soup(input)
    with open("data_file.json", "w", encoding='utf-8') as write_file:
        json.dump(get_products(soup, input), write_file, ensure_ascii=False)

main('https://www.dji.com/ru')