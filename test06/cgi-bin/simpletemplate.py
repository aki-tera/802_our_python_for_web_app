#!python3

import re

if_pat = re.compile("¥$if¥s+(.*¥:)")
endif_pat = re.compile("¥$endif")
for_pat = re.compile("¥$for¥s+(.*)¥s+in¥s+(.*¥:)")
endfor_pat = re.compile("¥$endfor")
value_pat = re.compile("¥${(.+?)}")


class SimpleTemplate(object):
    """シンプルな機能をもつテンプレートエンジン

    Args:
        object ([type]): [description]
    """

    def __init__(self, body="", file_path=None):
        """初期化メソッド

        Args:
            body (str, optional): [description]. Defaults to "".
            file_path ([type], optional): [description]. Defaults to None.
        """
        if file_path:
            with open(file_path, "r") as f:
                body = f.read()
        body = body.replace("\r\n", "\n")
