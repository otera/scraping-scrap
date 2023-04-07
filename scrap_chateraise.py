import requests
import csv
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 403回避
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def no_product():
    return "※該当商品はオンラインでの取り扱い終了か取得失敗"


def get_details_icebar(target):
    response = requests.get(
        "https://www.chateraise.co.jp/" + target, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    goods_item_infos = soup.find_all(
        'div', {'class': 'block-goods-item-info'})
    for goods_item_info in goods_item_infos:
        dl_list = goods_item_info.find_all('dl')
        for dl in dl_list:
            dt = dl.find('dt').text
            dd = dl.find('dd').text
            print(dt)
            print(dd)


def get_target_icebar():
    # ターゲットURL
    target = "https://www.chateraise.co.jp/ec/c/cice-bar/"
    response = requests.get(target, headers=headers)

    # BeautifulSoupオブジェクトを作成
    soup = BeautifulSoup(response.text, "html.parser")
    pickup_items = soup.find("ul", {"class": "block-pickup-list-p--items"})

    # li要素を出力
    for item in pickup_items.find_all("li"):
        name = item.find("a", {
            "class": 'js-enhanced-ecommerce-goods-name'}).text
        price = item.find("div", {
                          "class": 'block-pickup-list-p--price price js-enhanced-ecommerce-goods-price'}).text
        detail_url = item.find(
            "a", {"class": 'js-enhanced-ecommerce-goods-name'}).get('href')

        print(name, price, detail_url)


get_target_icebar()


class Product:
    def __init__(self, name, price, spec):
        self.name = name
        self.price = price
        self.spec = spec

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_spec(self):
        return self.spec

    def set_name(self, name):
        self.name = name

    def set_price(self, price):
        self.price = price
