import string

import requests
import json

from bs4 import BeautifulSoup

DOMAIN = 'https://www.technodom.kz'
URL = 'https://www.technodom.kz/catalog/'


def get_catalogue_links(url: string) -> []:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    li_tags = soup.find_all('li', attrs='catalog-page__subcategory')
    fetched_urls = []

    for li in li_tags:
        a = li.find('a')
        href = a.get('href')
        fetched_urls.append(DOMAIN + href)

    return fetched_urls


def get_products_links(url: string) -> []:
    page = 1
    fetched_urls = []
    while True:
        page_url = url + f'?page={page}'
        print(page_url)
        response = requests.get(page_url)

        soup = BeautifulSoup(response.content, 'html.parser')

        if len(soup.find_all('a', attrs='category-page-list__item-link')) == 0:
            return fetched_urls

        ul_tags = soup.find('ul', attrs='category-page-list__list')
        links = ul_tags.find_all('a')
        for link in links:
            href = link.get('href')
            fetched_urls.append(DOMAIN + href)

        page += 1


def get_all_products(url: string) -> []:
    catalogue_links = get_catalogue_links(url)
    items = []
    for link in catalogue_links:
        print(link)
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        item = {}

        span_tags = soup.find_all('span', itemprop='name')
        if len(span_tags) == 4:
            item['category'] = span_tags[1].text
            item['subcategory'] = span_tags[2].text
            item['item_type'] = span_tags[3].text
        elif len(span_tags) == 3:
            item['category'] = span_tags[1].text
            item['subcategory'] = span_tags[2].text
        elif len(span_tags) == 2:
            item['category'] = span_tags[1].text

        item_links = get_products_links(link)
        for item_link in item_links:
            item['item_link'] = item_link
            items.append(item)

    return items


with open("links.json", "w") as outfile:
    json.dump(get_all_products(URL), outfile, indent=6)

