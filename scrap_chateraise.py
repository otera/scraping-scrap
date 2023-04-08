import requests
# import pandas as pd
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Product:
    def __init__(self, name, price, comment, spec):
        self.name = name
        self.price = price
        self.comment = comment
        self.spec = spec

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_comment(self):
        return self.comment

    def get_spec(self):
        return self.spec

    def set_name(self, name):
        self.name = name

    def set_price(self, price):
        self.price = price

    def set_comment(self, comment):
        self.comment = comment

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
    spec = {}

    soup = get_bs("https://www.chateraise.co.jp/" + target)

    # ここいらないかも
    # allergy = soup.find(
    #     'dl', {'class': 'goods-detail-description block-goods-attr3'})
    # # spec["アレルギー"] = allergy.find('dd').text
    # if allergy is not None:
    #     spec["アレルギー"] = allergy.find('dd').text
    # else:
    #     spec["アレルギー"] = "不明"

    comment = soup.find(
        "div", {"class": "block-goods-comment1"}).text.replace("\r\n", "").strip()

    goods_item_infos = soup.find_all(
        'div', {'class': 'block-goods-item-info'})
    for goods_item_info in goods_item_infos:
        dl_list = goods_item_info.find_all('dl')
        for dl in dl_list:
            dt = dl.find('dt').text
            dd = dl.find('dd').text
            spec[dt] = dd

    return comment, spec


# ページに表示されている商品情報をスクレイピングする
def get_target_icebar(soup):
    pickup_items = soup.find("ul", {"class": "block-pickup-list-p--items"})

    # デバッグ用
    for i, item in enumerate(pickup_items.find_all("li")):
        # 条件1
        if i >= 1:
            break

    # 本番用
    # for item in pickup_items.find_all("li"):
        name = item.find("a", {
            "class": 'js-enhanced-ecommerce-goods-name'}).text
        price = item.find("div", {
                          "class": 'block-pickup-list-p--price price js-enhanced-ecommerce-goods-price'}).text
        detail_url = item.find(
            "a", {"class": 'js-enhanced-ecommerce-goods-name'}).get('href')

        # 詳細情報を取得
        print("次の商品情報を取得します", name)
        comment, spec = get_details_icebar(detail_url)
        # comment = None
        # spec = None

        icebars.append(Product(name, price, comment, spec))


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

for icebar in icebars:
    with open("シャトレーゼ_アイスバー情報.md", mode="a", encoding='utf-8') as file:
        file.write('# {0}\n'.format(icebar.get_name()))

        file.write('## 価格\n{0}\n\n'.format(icebar.get_price()))

        file.write('## 栄養成分表示・アレルギー\n')
        spec = icebar.get_spec()
        _spec = ""
        if spec is not None:
            for k, v in spec.items():
                _spec += "- {}\n".format(k)
                _spec += "  - {}\n".format(v)
            file.write(_spec)
        else:
            file.write("※取得できませんでした")
        file.write('\n')

        file.write('## コメント\n{0}\n\n'.format(icebar.get_comment()))
