import sys
import io
import pickle

# 前回作ったプログラムをインポートする
from httphandler import Request, Response, get_htmltemplate

# デバッグ表示
import cgitb
cgitb.enable(display=1)

# 日本語を送受信する時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

form_body = """
<form method="POST" action="/cgi-bin/picklepole.py">
好きな軽量言語は？<br>
{0}
<input type="submit" value="送信"/>
</form>
"""

radio_parts = """
<input type="radio" name="language" value="{0}" />{0}
<div style="border-left: solid {1}em red; ">{1}</div>
"""

lang_dic = {}
try:
    with open("./favorite_langage.dat", "rb") as f:
        lang_dic = pickle.load(f)
except:
    pass


content = ""
req = Request()
if "language" in req.form:
    lang = req.form["language"].value
    test=req.form
    lang_dic[lang] = lang_dic.get(lang, 0)+1
    with open("./favorite_langage.dat", "wb") as f:
        pickle.dump(lang_dic, f)

for lang in ["perl", "PHP", "Python", "Ruby"]:
    num = lang_dic.get(lang, 0)
    content += radio_parts.format(lang, num)

res = Response()
body = form_body.format(content)
res.set_body(get_htmltemplate().format(body))
print(res)
print(req.form)
print("\r\n")