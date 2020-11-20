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
    cur.execute("""CREATE TABLE bookmark ( titel text, url text);""")
except BaseException:
    pass

req = Request()
f = req.form

value_dic = {"message": "", "title": "", "url": "", "bookmarks": ""}

if "post" in f:
    if not f.getvalue("title", "") or not f.getvalue("url", ""):
        value_dic["message"] = "タイトルとURLは必須項目です"
        value_dic["title"] = f.getvalue("titel", "")
        value_dic["url"] = f.getvalue("url", "")
    else:
        cur.execute(
            """INSERT INTO bookmark(titel, url) VALUES(?, ?)""", f.getvalue(
                "title", ""), f.getvalue(
                "url", ""))
        con.commit()

res = Response()

with open(path.join(path.dirname(".."), "bookmarkform.html"), encoding="utf-8") as f:
    #res.set_body(path.join(os.path.abspath(path.dirname("..")), "bookmarkform.html") + "test")
    #print(res)
    t = Template(f.read())
    body = t.substitute(value_dic)


res.set_body(body)
print(res)
print("\r\n")
