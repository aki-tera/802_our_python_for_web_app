import sys
import io
import sqlite3
from string import Template
from os import path


# 前回作ったプログラムをインポートする
from httphandler import Request, Response


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

# デバッグ用：開始
res = Response()
body = ""
for word, read in value_dic.items():
    body = body + word + ":" + read + "**  **"
res.set_body(body)
print(res)
# デバッグ用：終了

if "post" in f:
    if not f.getvalue("title", "") or not f.getvalue("url", ""):
        value_dic["message"] = "タイトルとURLは必須項目です"
    else:
        # INSERTする際の文字列は’’でくるらないとエラーが発生する
        cur.execute(
            """INSERT INTO bookmark(title, url) VALUES('{0}', '{1}')""".format(
                value_dic["title"],
                value_dic["url"]))
        con.commit()


res = Response()

listbody = ""
cur.execute("SELECT title, url FROM bookmark")
for item in cur.fetchall():
    # タプルで出力されるのでスライスする
    listbody += """<dt>{0}</dt><dd>{1}</dd>\n""".format(item[0], item[1])
listbody = """<ul>\n{0}</ul>""".format(listbody)
value_dic["bookmarks"] = listbody


# with構文に変更
with open(path.join(path.dirname(".."), "bookmarkform.html"), encoding="utf-8") as f:
    t = Template(f.read())
    body = t.substitute(value_dic)


res.set_body(body)
print(res)
print("\r\n")
