import subprocess
import io

from util import text_wrapper


class Mrph:
    def __init__(self, midasi, hinsi, bunrui):
        self.midasi = midasi
        self.hinsi= hinsi
        self.bunrui = bunrui


def jumanpp_parser(text):
    """
    音声認識結果をJumanにかけ、相槌可能かを判定する
    :return:
    """
    text = text.replace(' ', '　')  # Juman用に半角スペースを全角へ
    if len(text) < 3:
        return False

    # サーバーモードJuman++に送る
    cmd = 'echo "' + text + '" | ruby jumanpp_client.rb --host localhost'
    res = subprocess.run(cmd, shell=True, encoding='utf-8', stdout=subprocess.PIPE)

    # 表層形 読み 見出し語 品詞大分類 品詞大分類 ID 品詞細分類 品詞細分類 ID 活用型 活用型 ID 活用形 活用形 ID 意味情報
    juman_finalmrph = res.stdout.splitlines()[-2].split()
    final_mrph = Mrph(juman_finalmrph[2], juman_finalmrph[3], juman_finalmrph[5])  # 最終形態素の見出し語,品詞大分類,品詞細分類のみ

    # 相槌可能か
    if any([is_absolute_boundary(final_mrph), is_strong_boundary(final_mrph), is_week_boundary(final_mrph),
            is_special_mrph(text)]):
        return True
    return False


def is_absolute_boundary(mrph):
    """絶対境界について調べる"""
    if mrph.bunrui == "終助詞":
        print("【絶対境界】文末候補：終助詞：", mrph.midasi)
    else:
        return False
    return True


def is_strong_boundary(mrph):
    """強境界について調べる"""
    if mrph.midasi == "が" and mrph.hinsi == "助詞":
        print("【強境界】並列節ガ：", mrph.midasi)
    elif mrph.midasi == "けど":
        print("【強境界】並列節ケド：", mrph.midasi)
    elif mrph.midasi == "けども":
        print("【強境界】並列節ケドモ：", mrph.midasi)
    elif mrph.midasi == "けれど":
        print("【強境界】並列節ケレド：", mrph.midasi)
    elif mrph.midasi == "けれども":
        print("【強境界】並列節ケレドモ：", mrph.midasi)
    elif mrph.midasi == "し" and mrph.hinsi == "助詞":
        print("【強境界】並列節シ：", mrph.midasi)
    else:
        return False
    return True


def is_week_boundary(mrph):
    """弱境界について調べる"""
    # 弱境界
    if mrph.midasi == "たり" and mrph.hinsi == "助詞":
        print("【弱境界】タリ節：", mrph.midasi)
    elif mrph.midasi == "てから" and mrph.hinsi == "助詞":
        print("【弱境界】テカラ節：", mrph.midasi)
    elif mrph.midasi == "ては" and mrph.hinsi == "助詞":
        print("【弱境界】テハ節：", mrph.midasi)
    elif mrph.midasi == "ても" and mrph.hinsi == "助詞":
        print("【弱境界】テモ節：", mrph.midasi)
    elif mrph.midasi == "て" and mrph.hinsi == "助詞":
        print("【弱境界】テ節：", mrph.midasi)
    elif mrph.midasi == "という" and mrph.hinsi == "助詞":
        print("【弱境界】トイウ節：", mrph.midasi)
    elif mrph.midasi == "とか" and mrph.hinsi == "助詞":
        print("【弱境界】トカ節：", mrph.midasi)
    elif mrph.midasi == "のに" and mrph.hinsi == "助詞":
        print("【弱境界】ノニ節：", mrph.midasi)
    elif mrph.midasi == "ように" and mrph.hinsi == "助詞":
        print("【弱境界】ヨウニ節：", mrph.midasi)
    elif mrph.midasi == "との" and mrph.hinsi == "助詞":
        print("【弱境界】引用節トノ：", mrph.midasi)
    elif mrph.midasi == "たら" and mrph.hinsi == "助詞":
        print("【弱境界】条件節タラ：", mrph.midasi)
    elif mrph.midasi == "たらば" and mrph.hinsi == "助詞":
        print("【弱境界】引用節タラバ：", mrph.midasi)
    elif mrph.midasi == "と" and mrph.hinsi == "助詞":
        print("【弱境界】条件節ト：", mrph.midasi)
    elif mrph.midasi == "なら" and mrph.hinsi == "助詞":
        print("【弱境界】条件節ナラ：", mrph.midasi)
    elif mrph.midasi == "ならば" and mrph.hinsi == "助詞":
        print("【弱境界】条件節ナラバ：", mrph.midasi)
    elif mrph.midasi == "れば" and mrph.hinsi == "助詞":
        print("【弱境界】条件節レバ：", mrph.midasi)
    elif mrph.midasi == "だの" and mrph.hinsi == "助詞":
        print("【弱境界】並列節ダノ：", mrph.midasi)
    # elif mrph.midasi == "で" and mrph.hinsi == "助詞":
    #     print("【弱境界】条件節デ：", mrph.midasi)
    elif mrph.midasi == "なり" and mrph.hinsi == "助詞":
        print("【弱境界】並列節ナリ：", mrph.midasi)
    elif mrph.midasi == "から" and mrph.hinsi == "助詞":
        print("【弱境界】理由節カラ：", mrph.midasi)
    elif mrph.midasi == "からには" and mrph.hinsi == "助詞":
        print("【弱境界】理由節カラニハ：", mrph.midasi)
    elif mrph.midasi == "ので" and mrph.hinsi == "助詞":
        print("【弱境界】理由節ノデ：", mrph.midasi)
    elif mrph.midasi == "ての" and mrph.hinsi == "助詞":
        print("【弱境界】並列節テノ：", mrph.midasi)
    # elif mrph.hinsi == "感動詞":
    #    print("【弱境界】感動詞：", mrph.midasi)
    # elif mrph.hinsi == "接続詞":
    #     print("【弱境界】接続詞：", mrph.midasi)
    else:
        return False
    return True


def is_special_mrph(text):
    """JUMAN++で解析できない特殊な単語を調べる"""
    if "じゃん" in text:
        print("助詞 終助詞 ~じゃん")
    else:
        return False
    return True
