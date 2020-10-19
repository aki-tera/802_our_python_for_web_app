import io
import sys
import cgi

# 前回作ったプログラムをインポートする
from rssparser import parse_rss
from httphandler import Request, Response, get_htmltemplate


# デバッグ表示
import cgitb
cgitb.enable(display=1)

# 日本語を送受信する時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


form_body = """
<form method="POST" action="/cgi-bin/rssreader1.py">
  RSSのURL:
  <input type="text" size="40" name="url" value="{0}"/>
  <input type="submit" />
</form>"""

rss_parts = """
<h3><a href="{0[link]}">{0[title]}</a></h3>
<p>{0[description]}</p>
"""

content = "URLを入力してください"

req = Request()
if "url" in req.form:
    try:
        rss_list = parse_rss(req.form["url"].value)
        content = ""
        for d in rss_list:
            content += rss_parts.format(d)
    except:
        pass


res = Response()
body = form_body.format(req.form.getvalue("url", ""))
body += content
res.set_body(get_htmltemplate().format(body))
print(res)
print("\r\n")

