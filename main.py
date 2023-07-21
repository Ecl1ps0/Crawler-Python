from link_handler import LinkHandler

URL = 'https://www.technodom.kz/catalog/'
FILE_PATH = 'links.json'

handler = LinkHandler(URL, FILE_PATH)
handler.get_all_products()
