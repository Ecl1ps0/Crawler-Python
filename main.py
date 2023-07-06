import requests
import json

from bs4 import BeautifulSoup

DOMAIN = 'https://www.technodom.kz'
URL = 'https://www.technodom.kz/catalog/smartfony-i-gadzhety/smartfony-i-telefony/smartfony'


def crawl(url):
    page = 1
    fetched_urls = []
    while True:
        page_url = url + f'?page={page}'
        print(page_url)
        response = requests.get(page_url)

        soup = BeautifulSoup(response.content, 'html.parser')

        if soup.find('p', attrs='category-page-list__subtitle').text == 'Найдено 0 товаров':
            print(soup.find('p', attrs='category-page-list__subtitle').text)
            return fetched_urls

        ul = soup.find('ul', attrs='category-page-list__list')
        links = ul.find_all('a')
        for link in links:
            href = link.get('href')
            fetched_urls.append({'link': DOMAIN + href})
            print(href)

        page += 1


urls = crawl(URL)
JSON_string = json.dumps(urls)

with open("links.json", "w") as outfile:
    outfile.write(JSON_string)
