import time
from random import random
import requests
from bs4 import BeautifulSoup
from print_utils import *
from product import *
import pandas as pd

def scrape_brand(brand:Brand):
    result:list[dict] = []
    for page_index in range(30):
        print_info(f"Scraping {brand.value}, page {page_index}... ", end='')
        af_repr = brand.af_repr
        if af_repr is None: raise Exception("af_repr cannot be None")

        url = f'https://www.alwaysfashion.com/tr/{af_repr}?orderby=0&pagesize=24&viewmode=list&pagenumber={page_index}'

        response = requests.get(url)
        time.sleep(random() * 2 + 1) # to not get blacklisted from the website

        soup = BeautifulSoup(response.text, 'html.parser')
        product_items = soup.select('div.product-item')

        if len(product_items) == 0:
            print_info(f"Page {page_index} has no products. Aborting.")
            break

        for product_item in product_items:
            product_name = product_item.select_one("span.product-title > a").text
            product_name = product_name.strip().lower().replace(brand.value.lower(), '').replace(',','').strip()
            product_price = product_item.select_one("span.actual-price").text.split(',')[0].replace(".", "")
            product_link = "https://www.alwaysfashion.com" + product_item.select_one("span.product-title > a").get('href')
            product_category:Category = Category.OTHER
            if "dolma kalem" in product_name: product_category = Category.FOUNTAIN_PEN
            elif "roller kalem" in product_name: product_category = Category.ROLLERBALL_PEN
            elif "tükenmez kalem" in product_name: product_category = Category.BALLPOINT_PEN

            p = Product(product_name, int(product_price),
                              product_link, product_category, brand)

            result.append(p.__dict__())

        print_info("Done.")


    return result

visconti_products = scrape_brand(Brand.VISCONTI)
df = pd.DataFrame(visconti_products)
df.to_csv('visconti_products.csv', index=False)