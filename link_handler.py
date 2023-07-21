import json
import os

import requests
from bs4 import BeautifulSoup

from link_collector import LinkCollector


class LinkHandler:
    def __init__(self, url, file_path):
        self.collector = LinkCollector(url)
        self.file_path = file_path

    def get_all_products(self) -> None:
        catalogue_links = self.collector.get_catalogue_links()
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

                item_links = self.collector.get_products_links(link)

                if not item_links:
                    continue

                for item_link in item_links:
                    items.append({**item, 'item_link': item_link})

                if not os.path.exists(self.file_path):
                    with open(self.file_path, 'w') as outfile:
                        json.dump(items, outfile, indent=6)
                else:
                    with open(self.file_path, 'r') as outfile:
                        data = json.load(outfile)

                    data.append(items)

                    with open(self.file_path, 'w') as outfile:
                        json.dump(data, outfile, indent=6)

            except Exception as e:
                print("Error: ", str(e))