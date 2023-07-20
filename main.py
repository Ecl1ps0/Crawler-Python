import requests
import json
import os

from bs4 import BeautifulSoup

DOMAIN = 'https://www.technodom.kz'
URL = 'https://www.technodom.kz/catalog/'
FILE_PATH = 'links.json'


def get_catalogue_links(url: str) -> list[str]:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        li_tags = soup.find_all('li', attrs='catalog-page__subcategory')
        fetched_urls = []

        for li in li_tags:
            a = li.find('a')
            href = a.get('href')
            fetched_urls.append(DOMAIN + href)

        return fetched_urls
    except Exception as e:
        print("Error: ", str(e))


def get_products_links(url: str) -> list[str]:
    page = 1
    fetched_urls = []
    while True:
        try:
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
        except Exception as e:
            print("Error: ", str(e))


def get_all_products(url: str) -> None:
    catalogue_links = get_catalogue_links(url)
    for link in catalogue_links:
        print(link)
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            items = []
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

            if not item_links:
                continue

            for item_link in item_links:
                items.append({**item, 'item_link': item_link})

            if not os.path.exists(FILE_PATH):
                with open(FILE_PATH, 'w') as outfile:
                    json.dump(items, outfile, indent=6)
            else:
                with open(FILE_PATH, 'r') as outfile:
                    data = json.load(outfile)

                data.append(items)

                with open(FILE_PATH, 'w') as outfile:
                    json.dump(data, outfile, indent=6)

        except Exception as e:
            print("Error: ", str(e))


get_all_products(URL)
