import io
import sys
import cgi

# デバッグ表示
import cgitb
cgitb.enable(display=1)

# 日本語を送受信する時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

form = cgi.FieldStorage()

html_body = """
<html>
    <head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
    </head>
    <body>
        {0}
    </body>
</html>
"""

body_line = []
body = form.getvalue("body", "")

# 不要
# body = unicode(body, "utf-8", "ignore")

for cnt in range(0, len(body), 10):
    line = body[:10]
    line += "".join(["□" for i in range(len(line), 10)])
    body_line.append(line)
    body = body[10:]

body_line_v = ["□".join(reversed(x)) for x in zip(*body_line)]


print("Content-type: text/html; charset=utf-8")
print("\r\n\r\n")
print(html_body.format("<br>".join(body_line_v)))
print("<br>")
print("<form>")
print('<INPUT type="button" onClick="history.back();" value="戻る">')
print("</form>")
print("\r\n")
