import cgi
from datetime import datetime
import io
import sys

# デバッグ表示
import cgitb
cgitb.enable(display=1)

# 日本語を送受信する時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

html_body = """
<html>
    <head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
    </head>
    <body>
        <form method="GET" action="/cgi-bin/f13form.py">
        西暦を選んでください:
            <select name="year">
                {0}
            </select>
            <input type="submit" />
        </form>
        {1}
    </body>
</html>"""

options = ""
content = ""
now = datetime.now()

for y in range(now.year-10, now.year+10):
    if y != now.year:
        select = ""
    else:
        select = " selected='selected'"
    options += "<option{0}>{1}</option>".format(select, y)

form = cgi.FieldStorage()
year_str = form.getvalue("year", "")

if year_str.isdigit():
    year = int(year_str)
    friday13 = 0
    for month in range(1, 13):
        date = datetime(year, month, 13)
        if date.weekday() == 4:
            friday13 += 1
            content += "{0}年{1}月13日は金曜日です".format(year, date.month)
            content += "<br />"
    if friday13 != 0:
        content += "{0}年には合計{1}個の13日の金曜日があります".format(year, friday13)
    else:
        content += "{0}年には13日の金曜日がありません".format(year)


print("Content-type: text/html; charset=utf-8")
print("\r\n\r\n")
print(html_body.format(options, content))
print("\r\n")
