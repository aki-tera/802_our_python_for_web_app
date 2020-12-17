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
        self.lines = body.split("\n")
        self.sentences = ((if_pat, self.handle_if), (for_pat,
                                                     self.handle_for), (value_pat, self.handle_value),)

    def process(self,exit_pats=(), start_line=0, kws={}):
        """テンプレートのレンダリング処理をする

        Args:
            exit_pats (tuple, optional): [description]. Defaults to ().
            start_line (int, optional): [description]. Defaults to 0.
            kws (dict, optional): [description]. Defaults to {}.
        """
