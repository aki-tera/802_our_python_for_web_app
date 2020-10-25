import xml.etree.ElementTree as ET
import urllib.request


def parse_rss(url):
    """
    RSS2.0をパースして、辞書のリストを返す
    """
    # RSSデータを取得
    with urllib.request.urlopen(url) as response:
        XmlData = response.read()
    # ルート要素を取得(Element型)
    root = ET.fromstring(XmlData)

    rsslist = []

    # RSS2.0のitemエレメントだけ抜き出す
    # in演算子は ==と違って文字列の中に対象が入っていればTrueとなる
    # "TEST" == "TE"  -> False
    # "TEST" in "TE"  -> False
    # "TE"   in "TEST"-> True
    # getiterator()は非推奨なので、iter()に変更
    for item in [x for x in root.iter() if "item" in x.tag]:
        rssdict = {}
        # 全ての要素を取り出す
        for elem in item.iter():
            for k in ["link", "title", "description", "author", "pubData"]:
                if k in elem.tag:
                    # 辞書を登録する
                    rssdict[k] = elem.text
                else:
                    # 不要なタグはN/Aで登録する
                    rssdict[k] = rssdict.get(k, "N/A")
        # 各々登録した辞書をリストにまとめる
        rsslist.append(rssdict)
    return(rsslist)
