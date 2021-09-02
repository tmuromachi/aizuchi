import subprocess
import io
import pandas as pd


# subprocessとして動作させた場合のデータをパージング
class Mrph:
    def __init__(self, midasi, hinsi, bunrui):
        self.midasi = midasi
        self.hinsi= hinsi
        self.bunrui = bunrui


# cmd = "ls -la"
cmd = 'echo "今夜はカレーよ" | ruby ../../src/web/jumanpp_client.rb --host localhost'
res = subprocess.run(cmd, shell=True, encoding='utf-8', stdout=subprocess.PIPE)
print(res.stdout)
print("------")
result_list = res.stdout.splitlines()
print(result_list)

print("------")
df = pd.read_csv(io.StringIO(res.stdout), header=None, sep=' ')
print(df)
df.drop(df.index[-1], axis=0)  # EOS削除
# print(df)
# 表層形 読み 見出し語 品詞大分類 品詞大分類ID 品詞細分類 品詞細分類ID 活用型 活用型 ID 活用形 活用形 ID 意味情報
final_mrph_midasi = df.iat[-2, 2]  # 見出し語
final_mrph_hinsi = df.iat[-2, 3]  # 品詞大分類
final_mrph_bunrui = df.iat[-2, 5]  # 品詞細分類
print("見出し語:", final_mrph_midasi)
print("品詞:", final_mrph_hinsi)
print("品詞細分類:", final_mrph_bunrui)

final_mrph = Mrph(df.iat[-2, 2], df.iat[-2, 3], df.iat[-2, 5])  # 最終形態素の見出し語,品詞大分類,品詞細分類のみ

print(final_mrph.midasi)

# pandas使わないやり方
text = "今夜はカレーよ"
print("->", len(text))
print(res.stdout.splitlines()[-2])
finalmrph = res.stdout.splitlines()[-2].split()
print(finalmrph)
print(finalmrph[2], finalmrph[3], finalmrph[5])

# mrph_list = result.mrph_list()
# "見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s"
# mrph.midasi,mrph.yomi,mrph.genkei,mrph.hinsi,mrph.bunrui,mrph.katuyou1,mrph.katuyou2,mrph.imis,mrph.repname
# final_mrph = mrph_list[-1]
# 表層形 読み 見出し語 品詞大分類 品詞大分類 ID 品詞細分類 品詞細分類 ID 活用型 活用型 ID 活用形 活用形 ID 意味情報
# midasi / mrph.hinsi / テキスト全体(これは問題なさそう)
