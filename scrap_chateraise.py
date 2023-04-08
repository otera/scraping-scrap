import requests
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Product:
    """
    商品情報

    Attributes:
        name (str): 商品名
        price (str): 価格
        comment (str): 紹介文
        spec(dict): 栄養成分表
    """

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


def get_bs(url):
    # 403回避
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")


def get_icebar_details(target):
    """
    アイスバーの詳細情報を取得する

    Parameters:
        target (str): 各アイスバーの詳細ページURL

    Returns:
        Tuple[str, Dict[str, str]]: 商品説明文、栄養成分表
    """

    spec = {}

    soup = get_bs("https://www.chateraise.co.jp/" + target)

    comment_selector = "div.block-goods-comment1"
    comment = soup.select_one(
        comment_selector).text.strip().replace("\r\n", "")

    item_selector = "div.block-goods-item-info dl"
    item_details = soup.select(item_selector)
    for item in item_details:
        dt = item.select_one("dt").text
        dd = item.select_one("dd").text
        spec[dt] = dd.strip()

    return comment, spec


def get_target_icebar(soup):
    """
    検索結果一覧のsoupから、各商品情報を取得する

    Parameters:
        soup (bs4.BeautifulSoup): 商品情報が含まれるWebページの BeautifulSoup オブジェクト
    """

    pickup_list = soup.select_one("ul.block-pickup-list-p--items")

    for pickup_item in pickup_list.select("li"):
        name_elem = pickup_item.select_one(
            "a.js-enhanced-ecommerce-goods-name")
        name = name_elem.text

        price = pickup_item.select_one(
            "div.block-pickup-list-p--price.price.js-enhanced-ecommerce-goods-price").text

        detail_url = name_elem.get("href")

        print("次の商品情報を取得します", name)
        comment, spec = get_icebar_details(detail_url)

        icebars.append(Product(name, price, comment, spec))


# スクレイピング処理
icebars = []
target_url = "https://www.chateraise.co.jp/ec/c/cice-bar/"
while True:
    soup = get_bs(target_url)

    # 必要な情報をスクレイピング
    get_target_icebar(soup)

    # 次のページがなければ処理終了
    next_link = soup.select_one("li.pager-next > a")
    if not next_link:
        break

    # 次のページのURLを生成する
    target_url = "https://www.chateraise.co.jp/" + next_link["href"]

# スクレイピング結果をファイルに書き出す
for icebar in icebars:
    with open("シャトレーゼ_アイスバー情報.md", mode="a", encoding='utf-8') as file:
        file.write('# {0}\n'.format(icebar.get_name()))

        file.write('## 価格\n{0}\n\n'.format(icebar.get_price()))

        file.write('## 栄養成分表示・アレルギー\n')
        spec = icebar.get_spec()
        _spec = ""
        for k, v in spec.items():
            _spec += "- {}\n".format(k)
            _spec += "  - {}\n".format(v)
        file.write('{}\n'.format(_spec))

        file.write('## コメント\n{0}\n\n'.format(icebar.get_comment()))
