import logging

import requests
from bs4 import BeautifulSoup

from config import logger


class LinkCollector:
    def __init__(self, url):
        self.url = url
        self.domain = 'https://www.technodom.kz'

    def get_catalogue_links(self) -> list[str]:
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(str(e))

        try:
            li_tags = soup.find_all('li', attrs='catalog-page__subcategory')
        except AttributeError as e:
            logger.error(str(e))
            li_tags = []

        fetched_urls = []
        for li in li_tags:
            a = li.find('a')
            href = a.get('href')
            fetched_urls.append(self.domain + href)

        return fetched_urls

    def get_products_links(self, page_link: str) -> list[str]:
        page = 1
        fetched_urls = []
        while True:
            page_url = page_link + f'?page={page}'
            print(page_url)

            try:
                response = requests.get(page_url)
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                logging.error(str(e))

            if len(soup.find_all('a', attrs='category-page-list__item-link')) == 0:
                return fetched_urls

            try:
                ul_tags = soup.find('ul', attrs='category-page-list__list')
                links = ul_tags.find_all('a')
            except AttributeError as e:
                logger.error(str(e))
                links = []

            for link in links:
                href = link.get('href')
                fetched_urls.append(self.domain + href)

            page += 1
