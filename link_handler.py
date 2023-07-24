import json
import os

import requests
from bs4 import BeautifulSoup

from link_collector import LinkCollector
from config import link_handler_logger


class LinkHandler:
    def __init__(self, url, file_path):
        self.collector = LinkCollector(url)
        self.file_path = file_path

    def get_all_products(self) -> None:
        link_handler_logger.info("Start forming list of items ot JSON format")

        for link in self.collector.get_catalogue_links():
            link_handler_logger.info(f"Current link: {link}")

            try:
                response = requests.get(link)
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                link_handler_logger.error(str(e))

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

            for item_link in self.collector.get_products_links(link):
                items.append({**item, 'item_link': item_link})

            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w') as outfile:
                    json.dump(items, outfile, indent=6)
            else:
                with open(self.file_path, 'r') as outfile:
                    data = json.load(outfile)

                for item in items:
                    data.append(item)

                with open(self.file_path, 'w') as outfile:
                    json.dump(data, outfile, indent=6)

        link_handler_logger.info("End forming list of items ot JSON format")
