import enum


class Features(enum.Enum):
    # ==文節品詞==
    is_n_v_a = enum.auto()  # 名詞，動詞，形容詞が存在するか    (auto()は1から開始)
    noun = enum.auto()  # 名詞
    demonstrative = enum.auto()  # 指示詞
    verb = enum.auto()  # 動詞
    adjective = enum.auto()  # 形容詞
    judgment = enum.auto()  # 判定詞
    auxiliary_verb = enum.auto()  # 助動詞
    adverb = enum.auto()  # 副詞
    particle = enum.auto()  # 助詞
    conjunction = enum.auto()  # 接続詞
    adnominal_adjective = enum.auto()  # 連体詞
    interjection = enum.auto()  # 感動詞
    prefix = enum.auto()  # 接頭詞
    suffix = enum.auto()  # 接尾辞
    pos_other = enum.auto()  # 特殊、未定義語

    # ==節境界==
    absolute_boundary = enum.auto()  # 絶対境界があるかどうか
    strong_boundary = enum.auto()  # 強境界があるかどうか
    week_boundary = enum.auto()  # 弱境界があるかどうか
    # 強境界
    ga = enum.auto()  # 【強境界】並列節ガ
    kedo = enum.auto()  # 【強境界】並列節ケド
    kedomo = enum.auto()  # 【強境界】並列節ケドモ
    keredo = enum.auto()  # 【強境界】並列節ケレド
    keredomo = enum.auto()  # 【強境界】並列節ケレドモ
    shi = enum.auto()  # 【強境界】並列節シ
    # 弱境界
    tari = enum.auto()  # 【弱境界】タリ節
    tekara = enum.auto()  # 【弱境界】テカラ節
    teha = enum.auto()  # 【弱境界】テハ節
    temo = enum.auto()  # 【弱境界】テモ節
    te = enum.auto()  # 【弱境界】テ節
    toiu = enum.auto()  # 【弱境界】トイウ節
    toka = enum.auto()  # 【弱境界】トカ節
    noni = enum.auto()  # 【弱境界】ノニ節
    youni = enum.auto()  # 【弱境界】ヨウニ節
    tono = enum.auto()  # 【弱境界】引用節トノ
    tara = enum.auto()  # 【弱境界】条件節タラ
    taraba = enum.auto()  # 【弱境界】条件節タラバ
    to = enum.auto()  # 【弱境界】条件節ト
    nara = enum.auto()  # 【弱境界】条件節ナラ
    naraba = enum.auto()  # 【弱境界】条件節ナラバ
    reba = enum.auto()  # 【弱境界】条件節レバ
    dano = enum.auto()  # 【弱境界】並列節ダノ
    de = enum.auto()  # 【弱境界】条件節デ
    nari = enum.auto()  # 【弱境界】並列節ナリ
    kara = enum.auto()  # 【弱境界】理由節カラ
    karaniha = enum.auto()  # 【弱境界】理由節カラニハ
    node = enum.auto()  # 【弱境界】理由節ノデ
    teno = enum.auto()  # 【弱境界】並列節テノ
    interjection_pos = enum.auto()  # 【弱境界】感動詞
    conjunction_pos = enum.auto()  # 【弱境界】接続詞
    # 絶対境界
    final_particle = enum.auto()  # 【絶対境界】文末候補：終助詞

    # 母音の引き伸ばし
    is_mora_long = enum.auto()  # 最後に「：」があるかどうか

    # 発話速度
    is_utterance_speed_fast = enum.auto()  # 平均より遅いか早いか
    utterance_speed = enum.auto()  # 読みの文字数


# test用
if __name__ == '__main__':
    print(Features.noun)
    print(Features(1))
    print(Features.noun.value)
    if Features.noun.value == 2:
        print("features value == int")
    print(len(Features))

# ==============================================================
# ==文節品詞==
# 名詞，動詞，形容詞が存在するか
# 名詞
# 指示詞
# 動詞
# 形容詞
# 判定詞
# 助動詞
# 副詞
# 助詞
# 接続詞
# 連体詞
# 感動詞
# 接頭詞
# 接尾辞
# 特殊
# 未定義語

# ==節境界データセット==
# 0：絶対境界かどうか
# 1：強境界かどうか
# 2：弱境界かどうか
# 強境界
# 3：【強境界】並列節ガ
# 4：【強境界】並列節ケド
# 5：【強境界】並列節ケドモ
# 6：【強境界】並列節ケレドモ
# 7：【強境界】並列節シ
# 8：【弱境界】タリ節
# 9：【弱境界】テカラ節
# 10：【弱境界】テハ節
# 11：【弱境界】テモ節
# 12：【弱境界】テ節
# 13：【弱境界】トイウ節
# 14：【弱境界】トカ節
# 15：【弱境界】ノニ節
# 16：【弱境界】ヨウニ節
# 17：【弱境界】テモ節
# 18：【弱境界】条件節ト
# 19：【弱境界】条件節ナラ
# 20：【弱境界】並列節ダノ
# 21：【弱境界】条件節デ
# 22：【弱境界】並列節ナリ
# 23：【弱境界】理由節カラ
# 24：【弱境界】理由節カラニハ
# 25：【弱境界】理由節ノデ
# 26：【弱境界】並列節テノ
# 27：【弱境界】感動詞
# 28：【弱境界】接続詞
# 29：【絶対境界】文末候補：終助詞
