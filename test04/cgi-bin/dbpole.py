import sys
import io
import sqlite3

# 前回作ったプログラムをインポートする
from httphandler import Request, Response, get_htmltemplate

# デバッグ表示
import cgitb
cgitb.enable(display=1)

# 日本語を送受信する時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

form_body = """
<form method="POST" action="/cgi-bin/dbpole.py">
好きな軽量言語は？<br>
{0}
<input type="submit" value="送信"/>
</form>
"""

radio_parts = """
<input type="radio" name="language" value="{0}" />{0}
<div style="border-left: solid {1}em red; ">{1}</div>
"""


def incrementvalue(cur, lang_name):
    cur.execute(
        """SELECT value FROM language_pole Where name='{0}'""".format(lang_name))

    item = None
    for item in cur.fetchall():
        cur.execute(
            """UPDATE language_pole SET value={0} WHERE name='{1}'""".format(
                item[0] + 1, lang_name))
    if not item:
        cur.execute(
            """INSERT INTO language_pole(name, value) VALUES('{0}', 1)""".format(lang_name))


con = sqlite3.connect("./dbfile.dat")
# con = sqlite3.connect(":memory:")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE language_pole (name text, value int);""")
except BaseException:
    pass

content = ""
req = Request()
test = 1

if "language" in req.form:
    incrementvalue(cur, req.form["language"].value)
    test = 0

lang_dic = {}
cur.execute("""SELECT name, value FROM language_pole;""")
for res in cur.fetchall():
    lang_dic[res[0]] = res[1]

for lang in ['Perl', 'PHP', 'Python', 'Ruby']:
    num = lang_dic.get(lang, 0)
    content += radio_parts.format(lang, num)

con.commit()
res = Response()
body = form_body.format(content)
res.set_body(get_htmltemplate().format(body))
print(res)
print(req.form, test)
cur.execute("""SELECT name, value FROM language_pole;""")
print("sqlite3:", cur.fetchall())
print("\r\n")
