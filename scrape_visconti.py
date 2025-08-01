import time
from random import random
import requests
from bs4 import BeautifulSoup
from print_utils import *
from product import *
import pandas as pd

products: list[dict[str, str]] = []

def calc_page_count():
    print_info("Calculating page count... ", '')
    url_ = f"https://www.viscontiturkey.com/kategori/kalem"
    response_ = requests.get(url_)
    soup_ = BeautifulSoup(response_.text, 'html.parser')
    text_el = soup_.select_one("div.record-count").text.strip().replace('\n','')
    product_count = int(text_el.split(" ")[1])
    page_count = (product_count // 30) + 1
    print_info('Done.')
    return page_count

for page_index in range(1, calc_page_count() + 1):
    print_info(f"Scraping page {page_index}... ", end='')
    url = f"https://www.viscontiturkey.com/kategori/kalem?tp={page_index}"
    response = requests.get(url)
    time.sleep(random() * 2 + 1)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_items = soup.select('div.showcase')

    if len(product_items) == 0:
        print_info(f"Page {page_index} has no products. Aborting.")
        break

    for product_item in product_items:
        product_name: str = (product_item.select_one('div.showcase-content > div.showcase-title > a').
                             text.lower().replace(',', '').strip())
        product_price: int = int(product_item.
                              select_one('div.showcase-content > div.showcase-price > div.showcase-price-new').
                              text.split(',')[0].replace('.',''))
        product_link = "https://www.viscontiturkey.com" + product_item.select_one('div.showcase-content > div.showcase-title > a').get('href')
        product_category: Category = Category.OTHER
        if "fp" in product_name: product_category = Category.FOUNTAIN_PEN
        elif "rb" in product_name: product_category = Category.ROLLERBALL_PEN
        elif "bp" in product_name: product_category = Category.BALLPOINT_PEN

        p = Product(product_name, int(product_price),
                    product_link, product_category,
                    Brand.VISCONTI)

        products.append(p.__dict__())
    print_info("Done.")

df = pd.DataFrame(products)
df.to_csv("visconti_products.csv", index=False)