import textwrap


def text_wrapper(text, n):
    """
    文字列を受け取って折り返す
    :param text:テキスト
    :param n:折り返す文字数
    :return:
    """
    wrap_text_list = textwrap.wrap(text, n)
    # text = '\n'.join(wrap_text_list)
    text = '<br>'.join(wrap_text_list)

    # 3行超えたら1行削除
    if text.count('<br>') > 3:
        text_split_list = text.split('<br>')
        text = text_split_list[-3] + '<br>' + text_split_list[-2] + '<br>' + text_split_list[-1]
        if '【相槌可能】' in text and text.count('<br>') > 4:
            text = text_split_list[-3] + '<br>' + text

    return text


def text_wrapper_test():
    print(text_wrapper("マイクテストです。マイクテストです！マイクテストです〜", 3))
    print(text_wrapper("マイクテストです。マイクテストです！マイクテストです〜【相槌可能】", 3))


if __name__ == '__main__':
    text_wrapper_test()    # テスト用