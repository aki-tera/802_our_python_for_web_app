import sys
import io
import sqlite3
from string import Template
from os import path
import os

# 前回作ったプログラムをインポートする
from httphandler import Request, Response, get_htmltemplate


# デバッグ表示
import cgitb
cgitb.enable(display=1)

# 日本語を送受信する時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

con = sqlite3.connect("./bookmark.dat")
cur = con.cursor()
try:
    cur.execute("""CREATE TABLE bookmark (title text, url text);""")
except BaseException:
    pass

req = Request()
f = req.form
value_dic = {"message": "", "title": "", "url": "", "bookmarks": ""}

# 辞書に値を入れるように追加
for key in value_dic:
    value_dic[key] = f.getvalue(key, "")

# デバッグ用
res = Response()
body = ""
for word, read in value_dic.items():
    body = body + word + ":" + read + "**  **"
res.set_body(body)
print(res)

if "post" in f:
    if not f.getvalue("title", "") or not f.getvalue("url", ""):
        value_dic["message"] = "タイトルとURLは必須項目です"
    else:
        # 現在の問題点は文字入力ができないこと
        cur.execute(
            """INSERT INTO bookmark(title, url) VALUES({0}, {1})""".format(
                value_dic["title"],
                str(value_dic["url"])))
        con.commit()


res = Response()

# with構文に変更
with open(path.join(path.dirname(".."), "bookmarkform.html"), encoding="utf-8") as f:
    t = Template(f.read())
    body = t.substitute(value_dic)


res.set_body(body)
print(res)
print("\r\n")
