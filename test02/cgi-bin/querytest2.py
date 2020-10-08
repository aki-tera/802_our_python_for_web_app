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

content = ""

for cnt, item in enumerate(form.getlist("language")):
    content += "{0}：{1} <br>".format(cnt+1, item)

print("Content-type: text/html; charset=utf-8")
print("\r\n\r\n")
print(html_body.format(content))
print("<br>")
print("<form>")
print('<INPUT type="button" onClick="history.back();" value="戻る">')
print("</form>")
print("\r\n")
