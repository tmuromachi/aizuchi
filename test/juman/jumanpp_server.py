from JapaneseTokenizer import JumanppWrapper

sentence = 'テヘラン（ペルシア語: تهران  ; Tehrān Tehran.ogg 発音[ヘルプ/ファイル]/teɦˈrɔːn/、英語:Tehran）は、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
sentence = 'こんにちは！'
list_result = JumanppWrapper(server='localhost', port=12000).tokenize(sentence, return_list=True, is_feature=True,
                                                                      is_surface=True)
# jumanpp_wrapper = JumanppWrapper()
print(list_result)
# seq_tokens_jumanpp = jumanpp_wrapper.tokenize(sentence=sentence, is_feature=False, is_surface=False).convert_list_object()
# print(seq_tokens_jumanpp)
