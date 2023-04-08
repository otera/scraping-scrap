import requests
import csv
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


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

    def set_spec(self, spec):
        self.spec = spec


def no_product():
    return "※該当商品はオンラインでの取り扱い終了か取得失敗"


def get_bs(url):
    # 403回避
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")


def get_details_icebar(target):
    details = {}

    soup = get_bs("https://www.chateraise.co.jp/" + target)

    allergy = soup.find(
        'dl', {'class': 'goods-detail-description block-goods-attr3'})
    details["アレルギー"] = allergy.find('dd').text

    goods_item_infos = soup.find_all(
        'div', {'class': 'block-goods-item-info'})
    for goods_item_info in goods_item_infos:
        dl_list = goods_item_info.find_all('dl')
        for dl in dl_list:
            dt = dl.find('dt').text
            dd = dl.find('dd').text
            details[dt] = dd

    return details


# ページに表示されている商品情報をスクレイピングする
def get_target_icebar(soup):
    pickup_items = soup.find("ul", {"class": "block-pickup-list-p--items"})
    for item in pickup_items.find_all("li"):
        name = item.find("a", {
            "class": 'js-enhanced-ecommerce-goods-name'}).text
        price = item.find("div", {
                          "class": 'block-pickup-list-p--price price js-enhanced-ecommerce-goods-price'}).text
        detail_url = item.find(
            "a", {"class": 'js-enhanced-ecommerce-goods-name'}).get('href')

        # 詳細情報を取得
        # spec = get_details_icebar(detail_url)
        spec = None

        icebars.append(Product(name, price, spec))


icebars = []
target_url = "https://www.chateraise.co.jp/ec/c/cice-bar/"
while True:
    soup = get_bs(target_url)

    # 必要な情報をスクレイピング
    get_target_icebar(soup)

    # 次のページがあるかどうかを確認する
    next_link = soup.find('li', {"class": 'pager-next'})
    if next_link is None:
        break

    # 次のページの URL を生成する
    next_link.find("a")

    target_url = "https://www.chateraise.co.jp/" + next_link.find("a")['href']
