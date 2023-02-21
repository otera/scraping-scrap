rows = ["<label><span>商品番号：187883</span></label>,"
"<label>1本 / <span>本体価格</span> 60円 <span>（税込 64円）【通販取扱なし】</span></label>",
"<label><span>商品番号：187885</span></label>",
"<label>6本入 / <span>本体価格</span> 280円 <span>（税込 302円）</span></label>"]

lst = list(filter(lambda x: "本体価格" in x, rows))
print("lst", lst)

