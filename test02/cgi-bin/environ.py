import io
import sys
import cgi

# デバッグ表示
import cgitb
cgitb.enable(display=1)

# 日本語を送受信する時にエラーにならないようにする為に必要。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("Content-type: text/html; charset=utf-8")
print("\r\n\r\n")
print(cgi.print_environ())
print("<br>")
print("<form>")
print('<INPUT type="button" onClick="history.back();" value="戻る">')
print("</form>")
print("\r\n")
