import logging
from typing import Generator

import requests
from bs4 import BeautifulSoup

from config import link_collector_logger


class LinkCollector:
    def __init__(self, url):
        self.url = url
        self.domain = 'https://www.technodom.kz'

    def get_catalogue_links(self) -> Generator[str, None, None]:
        link_collector_logger.info("Start collecting catalogue links")

        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            link_collector_logger.error(str(e))

        link_collector_logger.info(f"Start link: {self.url}")

        try:
            li_tags = soup.find_all('li', attrs='catalog-page__subcategory')
        except AttributeError as e:
            link_collector_logger.error(str(e))
            link_collector_logger.warning("li_tags variable has been changed to empty list")
            li_tags = []

        for li in li_tags:
            a = li.find('a')
            href = a.get('href')
            link_collector_logger.info(f"Current link: {self.domain + href}")
            yield self.domain + href

        link_collector_logger.info("End getting catalogue links")

    def get_products_links(self, page_link: str) -> Generator[str, None, None]:
        link_collector_logger.info("Start collecting items' links")

        page = 1
        while True:
            page_url = page_link + f'?page={page}'
            link_collector_logger.info(f"Current page link: {page_url}")

            try:
                response = requests.get(page_url)
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                logging.error(str(e))

            if len(soup.find_all('a', attrs='category-page-list__item-link')) == 0:
                link_collector_logger.info(f"End collecting items' links")
                return

            try:
                ul_tags = soup.find('ul', attrs='category-page-list__list')
                links = ul_tags.find_all('a')
            except AttributeError as e:
                link_collector_logger.error(str(e))
                links = []

            for link in links:
                href = link.get('href')
                yield self.domain + href

            page += 1
