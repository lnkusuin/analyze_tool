import functools
import pickle

import pandas as pd
from joblib import Parallel, delayed

from common import get_logger
from context.lda.common import load_state

logger = get_logger(__file__)


def run(
        texts_path="",
        corpus_path="",
        dictionary_path="",
        model_path="",
):
    texts, corpus, dictionary, model = load_state(
        text_path=texts_path,
        corpus_path=corpus_path,
        dictionary_path=dictionary_path,
        model_path=model_path
    )

    logger.info("既存テキストの振り分けを行います。")

    count = 0
    for text in texts:
        # other_corpus = [dictionary.doc2bow([text["lemma"] for text in text["words"]])]
        # print(other_corpus)
        other_corpus = [dictionary.doc2bow(text) for text in [text["nouns"]]]
        unseen_doc = other_corpus[0]
        vector = model[unseen_doc]

        vector = sorted(vector, key=lambda x: x[1], reverse=True)

        topic_id = vector[0][0] + 1
        ratio = vector[0][1]
        ratio_str = str("{:.2f}%").format(ratio * 100)

        if count % 1000 == 0:
            print(count)

        count += 1

        data = {
            "words": text["nouns"],
            "topic_id": topic_id,
            "ratio": ratio,
            "ratio_str": ratio_str,
            "hash_tags": text["hash_tags"],
            "text": text["text"]
        }

        yield corpus, dictionary, model, data

# def run(docs,
#         texts_path="../step3/t-TEXTS",
#         corpus_path="../step3/t-CORPUS_FILE_NAME",
#         dictionary_path="../step3/t-DICTIONARY",
#         model_path="../step3/t-Model-4"
#         ):
#
#     texts, corpus, dictionary, model = load_state(texts_path, corpus_path, dictionary_path, model_path)
#
#     for text in [
#         "12月のクリスマスver.の増田さんカレンダー作ってみました٩(๑^ᴗ^๑)۶✨🎄🎁",
#         "NEWSな2人から大事なお知らせ💫 明日の朝4時にTwitterをチェック @news2_tbs めっちゃめっちゃ期待していいのよね!!!!",
#         "かわゆい~💛💚 #NEWS #増田貴久 #加藤シゲアキ",
#         "SORASHIGE BOOK (∵)💚 新年早々お楽しみ増えたよ 💜💖💛💚 初回盤も通常盤もどちらも 魅力的(灬ºωº灬) #ソラシゲ #加藤シゲアキ  #EPCOTIA_ENCORE  #NEWS #EPCOTIA_ENCORE円盤化ありがとう",
#         "あした朝の4時？！( ﾟдﾟ)ﾊｯ! #NEWSな2人 #NEWS #小山慶一郎 #加藤シゲアキ",
#         "かわいすぎる！U R not alone 仲良し #NEWS のいいとこぎゅーーって詰まってるヽ(;▽;)ノ",
#         "ＷＡＤＡ ロシアへの処分決定 東京大会は個人資格参加のみに",
#         "【山形新聞】山響と教授、学生有志が共演　山形大70周年記念演奏会 ",
#         "【山形新聞】印象派に与えた影響ひもとく　山形美術館で「北斎づくし」記念講演 https://ift.tt/2qCyu34 #山形新聞 #yamashin #news",
#         "Amazonサイバーマンデーセール✨ 本日23:59まで⏰ 今年最後のビッグセール❗️ 最後まで目が離せない87時間👀 #サイバーマンデー #最大5000ポイント還元 #タイムセールも続々登場 #今年最後の最後",
#         "昨日のJuly Tech Festa 2019の登壇資料を公開しました！ https://slideshare.net/iwashi86/ss-203448193 #JTF2019 #JTF2019_E",
#         "解析力学入門に参加してみたが超面白かった。そして中井先生、説明がめちゃ上手いなー。#preNC",
#         "【最新ニュース】台風19号で浸水被害が出た埼玉県東松山市で、先月70代の男性が肺炎で死亡し、市は避難生活で体調が悪化した可能性が高いとして災害関連死と認定しました。埼玉県内で台風19号で死亡した人は合わせて４人となりました。 ＮＨＫニュース＆スポーツ http://nhknews.jp/p/ #nhk #news"
#     ]:
#         _text = CleanText(text).to_lower().to_adjust_line_code().to_remove_url().to_adjust_zero_number().to_adjust_mention().to_remove_symbol().text
#         doc = nlp()(_text, disable=['ner'])
#
#         other_texts = [token.lemma_ for token in doc]
#
#         other_corpus = [dictionary.doc2bow(text) for text in [other_texts]]
#         unseen_doc = other_corpus[0]
#         vector = model[unseen_doc]
#
#         vector = sorted(vector, key=lambda x: x[1], reverse=True)
#
#         topic_id = vector[0][0] + 1
#         ratio = vector[0][1]
#         ratio_str = str("{:.2f}%").format(ratio * 100)
#
#         if topic_id == 3 and ratio > 0.4:
#             print('ニュース(報道)', ratio_str, text)
#
#         elif (topic_id == 2 or topic_id == 1 or topic_id == 4) and ratio > 0.5:
#             print('ニュース(アイドル)', ratio_str, text)
#
#         else:
#             print("その他", ratio_str, text)
#
#
