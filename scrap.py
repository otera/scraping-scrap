import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def no_product():
    return "※該当商品はオンラインでの取り扱い終了"

# ターゲットURL情報を取得
targets = []
with open("./target.csv", "r", encoding="utf8", errors="", newline="" ) as csvFile:
    dic_reader = csv.DictReader(csvFile)
    for row in dic_reader:
        targets.append(row)

# ターゲットURL情報をもとに原材料などをスクレイピング
for target in targets:
    html = urlopen(target["url"])
    bsObj = BeautifulSoup(html, "html.parser")
    print("スクレイピング中：" + target["name"])

    # 同じidがあるから[1]で2行目取る
    relationInfo = bsObj.findAll("aside", {"id":"relation_info"})[1]
    rows = relationInfo.findAll("tr")
    with open("原材料情報情報.txt", mode="a", encoding='utf-8') as file:
        # 商品名書き出し
        file.write('●{0}\n'.format(target["name"]))

        # 商品情報が取得できているかどうか
        if not rows:
            # 取得できない場合は、オンラインでの取り扱いが終了として扱う
            file.write(no_product() + '\n')
        else:
            # 原材料等の情報を書き出す
            for row in rows:
                csvRow = []
                for cell in row.findAll(['td', 'th']):
                    csvRow.append(cell.get_text())
                file.write('【{0}】　{1}\n'.format(csvRow[0],csvRow[1]))

        # 1行スペース
        file.write('\n')
