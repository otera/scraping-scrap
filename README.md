Scraping Scrap
==================

Python(Beautiful Soup 4)を利用してWebスクレイピングを行う。

## Requirements

Python 3.9.10

## Usage

`target.csv`に成分表を取得したい商品のURLと商品名を記載する。

```csv
url,name
https://www.kaldi.co.jp/ec/pro/disp/1/4997540956644?sFlg=2,生ハム切り落とし
https://www.kaldi.co.jp/ec/pro/disp/1/4515996923623?sFlg=2,ブルスケッタ　ザク切りオリーブ　グリーン
```

スクレイピングの実行。

```bash
python scrap.py
```

`KALDIオンラインストアの原材料情報情報.txt`にスクレイピング結果が追記される。

## Install

仮想環境を作成&有効化し、`requirements.txt`を使ってパッケージをインストールする。  
Mac環境下では下記のようなコマンドを利用する。

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Windows11, Python3.11.1, Git bash

```bash
py -m venv env
source env/Scripts/activate
pip install -r requirements.txt
```
