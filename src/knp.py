from pyknp import Juman
from features import Features


def knp_parser(text):
    """
    音声認識結果をKNPにかけ、音声認識結果の最後の形態素を調査する。
    :return:
    """
    jumanpp = Juman()

    text = text.replace(' ', '　')  # KNP用に半角スペースを全角へ
    result = jumanpp.analysis(text)
    mrph_list = result.mrph_list()
    # print("--")
    # for mrph in mrph_list:  # 各形態素にアクセス
    #     print("見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
    #           % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis,
    #              mrph.repname))
    # print("--")
    # print(mrph_list[-1].midasi, mrph_list[-1].hinsi)
    final_mrph = mrph_list[-1]
    is_absolute_boundary(final_mrph)
    is_strong_boundary(final_mrph)
    is_week_boundary(final_mrph)
    is_special_mrph(mrph_list)
    # print("==========")


def is_absolute_boundary(mrph):
    """絶対境界について調べる"""
    if mrph.hinsi == "終助詞":
        print("【絶対境界】文末候補：終助詞：", mrph.midasi)


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
    elif mrph.midasi == "で" and mrph.hinsi == "助詞":
        print("【弱境界】条件節デ：", mrph.midasi)
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


def is_special_mrph(mrph_list):
    """JUMAN++で解析できない特殊な単語を調べる"""
    text = ""
    for mrph in mrph_list[-5:]:    # スライスだとIndex Error起きない
        text = text + mrph.midasi

    if "じゃん" in text:
        print("助詞 終助詞 ~じゃん")
