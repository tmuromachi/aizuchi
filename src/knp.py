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
    print("--")
    print(mrph_list[-1].midasi, mrph_list[-1].hinsi)
    final_mrph = mrph_list[-1]
    is_absolute_boundary(final_mrph)
    is_strong_boundary(final_mrph)
    is_week_boundary(final_mrph)
    print("==========")


def is_absolute_boundary(mrph):
    """絶対境界について調べる"""
    if mrph.hinsi == "終助詞":
        print("【絶対境界】文末候補：終助詞：", mrph.midasi)


def is_strong_boundary(mrph):
    """強境界について調べる"""
    if mrph.midasi == "が":
        print("【強境界】並列節ガ：", mrph.midasi)
    elif mrph.midasi == "けど":
        print("【強境界】並列節ケド：", mrph.midasi)
    elif mrph.midasi == "けども":
        print("【強境界】並列節ケドモ：", mrph.midasi)
    elif mrph.midasi == "けれど":
        print("【強境界】並列節ケレド：", mrph.midasi)
    elif mrph.midasi == "けれども":
        print("【強境界】並列節ケレドモ：", mrph.midasi)
    elif mrph.midasi == "し":
        print("【強境界】並列節シ：", mrph.midasi)


def is_week_boundary(mrph):
    """弱境界について調べる"""
    # 弱境界
    if mrph.midasi == "たり":
        print("【弱境界】タリ節：", mrph.midasi)
    elif mrph.midasi == "てから":
        print("【弱境界】テカラ節：", mrph.midasi)
    elif mrph.midasi == "ては":
        print("【弱境界】テハ節：", mrph.midasi)
    elif mrph.midasi == "ても":
        print("【弱境界】テモ節：", mrph.midasi)
    elif mrph.midasi == "て":
        print("【弱境界】テ節：", mrph.midasi)
    elif mrph.midasi == "という":
        print("【弱境界】トイウ節：", mrph.midasi)
    elif mrph.midasi == "とか":
        print("【弱境界】トカ節：", mrph.midasi)
    elif mrph.midasi == "のに":
        print("【弱境界】ノニ節：", mrph.midasi)
    elif mrph.midasi == "ように":
        print("【弱境界】ヨウニ節：", mrph.midasi)
    elif mrph.midasi == "との":
        print("【弱境界】引用節トノ：", mrph.midasi)
    elif mrph.midasi == "たら":
        print("【弱境界】条件節タラ：", mrph.midasi)
    elif mrph.midasi == "たらば":
        print("【弱境界】引用節タラバ：", mrph.midasi)
    elif mrph.midasi == "と":
        print("【弱境界】条件節ト：", mrph.midasi)
    elif mrph.midasi == "なら":
        print("【弱境界】条件節ナラ：", mrph.midasi)
    elif mrph.midasi == "ならば":
        print("【弱境界】条件節ナラバ：", mrph.midasi)
    elif mrph.midasi == "れば":
        print("【弱境界】条件節レバ：", mrph.midasi)
    elif mrph.midasi == "だの":
        print("【弱境界】並列節ダノ：", mrph.midasi)
    elif mrph.midasi == "で":
        print("【弱境界】条件節デ：", mrph.midasi)
    elif mrph.midasi == "なり":
        print("【弱境界】並列節ナリ：", mrph.midasi)
    elif mrph.midasi == "から":
        print("【弱境界】理由節カラ：", mrph.midasi)
    elif mrph.midasi == "からには":
        print("【弱境界】理由節カラニハ：", mrph.midasi)
    elif mrph.midasi == "ので":
        print("【弱境界】理由節ノデ：", mrph.midasi)
    elif mrph.midasi == "ての":
        print("【弱境界】並列節テノ：", mrph.midasi)

    elif mrph.hinsi == "感動詞":
        print("【弱境界】感動詞：", mrph.midasi)
    elif mrph.hinsi == "接続詞":
        print("【弱境界】接続詞：", mrph.midasi)


"""
def morph_check(self, mrph_list, features_df, index):
    # 形態素について調べる
    # 名詞，動詞，形容詞が存在するか
    if "名詞" in mrph_list[-1].hinsi or "動詞" in mrph_list[-1].hinsi or "形容詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.is_n_v_a.value] = 1

    if "名詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.noun.value] = 1
    elif "指示詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.demonstrative.value] = 1
    elif "動詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.verb.value] = 1
    elif "形容詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.adjective.value] = 1
    elif "判定詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.judgment.value] = 1
    elif "助動詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.auxiliary_verb.value] = 1
    elif "副詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.adverb.value] = 1
    elif "助詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.particle.value] = 1
    elif "接続詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.conjunction.value] = 1
    elif "連体詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.adnominal_adjective.value] = 1
    elif "感動詞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.interjection.value] = 1
    elif "接頭辞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.prefix.value] = 1
    elif "接尾辞" in mrph_list[-1].hinsi:
        features_df.iloc[index, Features.suffix.value] = 1
    else:
        features_df.iloc[index, Features.pos_other.value] = 1
    return features_df
"""