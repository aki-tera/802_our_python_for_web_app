import cgi

import sys
import io
# 日本語を受信時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

html_body = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
TEST
<p>
foo = {0}
<p>
hoo = {1}
</body>
</html>
"""

# (1)
form=cgi.FieldStorage()

print("Content-Type: text/html; charset=utf-8")

#引数が無い場合、N/Aを返す
print(html_body.format(form.getvalue("foo", "N/A"), form.getvalue("hoo", "N/A")))
