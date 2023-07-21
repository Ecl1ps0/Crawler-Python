import requests
from bs4 import BeautifulSoup


class LinkCollector:
    def __init__(self, url):
        self.url = url
        self.domain = 'https://www.technodom.kz'

    def get_catalogue_links(self) -> list[str]:
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')

            li_tags = soup.find_all('li', attrs='catalog-page__subcategory')
            fetched_urls = []

            for li in li_tags:
                a = li.find('a')
                href = a.get('href')
                fetched_urls.append(self.domain + href)

            return fetched_urls
        except Exception as e:
            print("Error: ", str(e))

    def get_products_links(self, page_link: str) -> list[str]:
        page = 1
        fetched_urls = []
        while True:
            try:
                page_url = page_link + f'?page={page}'
                print(page_url)
                response = requests.get(page_url)

                soup = BeautifulSoup(response.content, 'html.parser')

                if len(soup.find_all('a', attrs='category-page-list__item-link')) == 0:
                    return fetched_urls

                ul_tags = soup.find('ul', attrs='category-page-list__list')
                links = ul_tags.find_all('a')
                for link in links:
                    href = link.get('href')
                    fetched_urls.append(self.domain + href)

                page += 1
            except Exception as e:
                print("Error: ", str(e))
