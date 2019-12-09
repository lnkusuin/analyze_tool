import os
from pathlib import Path
import pickle

from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.dictionary import Dictionary

from nlp import CleanText
import gensim
from nlp import nlp
from common import get_logger

logger = get_logger(__file__)

def get_path(path):
    base_path = Path(os.path.dirname(__file__))
    return str(base_path / path)


def load_state(text_path, corpus_path, dictionary_path, model_path):
    """状態の復元"""

    logger.info("テキストを読み込みます")
    with open(get_path(text_path), "rb") as f:
        texts = pickle.load(f)

    logger.info("テキストの読み込みが完了しました。")

    logger.info("コーパスを読み込みます。")
    corpus = MmCorpus(get_path(corpus_path))
    # tfidf = gensim.models.TfidfModel(corpus)
    # corpus = tfidf[corpus]
    logger.info("コーパスの読み込みが完了しました。")

    logger.info("辞書を読み込みます。")
    dictionary = Dictionary.load(get_path(dictionary_path))
    logger.info("辞書の読み込みが完了しました。")

    logger.info("LDAを読み込みます。")
    model = gensim.models.ldamodel.LdaModel.load(get_path(model_path))
    logger.info("LDAの読み込みが完了しました。")

    return texts, corpus, dictionary, model


def run(docs,
        texts_path="../step3/t-TEXTS",
        corpus_path="../step3/t-CORPUS_FILE_NAME",
        dictionary_path="../step3/t-DICTIONARY",
        model_path="../step3/t-Model-2"
        ):

    texts, corpus, dictionary, model = load_state(texts_path, corpus_path, dictionary_path, model_path)

    for text in [
        "12月のクリスマスver.の増田さんカレンダー作ってみました٩(๑^ᴗ^๑)۶✨🎄🎁",
        "NEWSな2人から大事なお知らせ💫 明日の朝4時にTwitterをチェック @news2_tbs めっちゃめっちゃ期待していいのよね!!!!",
        "かわゆい~💛💚 #NEWS #増田貴久 #加藤シゲアキ",
        "SORASHIGE BOOK (∵)💚 新年早々お楽しみ増えたよ 💜💖💛💚 初回盤も通常盤もどちらも 魅力的(灬ºωº灬) #ソラシゲ #加藤シゲアキ  #EPCOTIA_ENCORE  #NEWS #EPCOTIA_ENCORE円盤化ありがとう",
        "ＷＡＤＡ ロシアへの処分決定 東京大会は個人資格参加のみに",
        "【山形新聞】山響と教授、学生有志が共演　山形大70周年記念演奏会 ",
        "【山形新聞】印象派に与えた影響ひもとく　山形美術館で「北斎づくし」記念講演 https://ift.tt/2qCyu34 #山形新聞 #yamashin #news",
        "Amazonサイバーマンデーセール✨ 本日23:59まで⏰ 今年最後のビッグセール❗️ 最後まで目が離せない87時間👀 #サイバーマンデー #最大5000ポイント還元 #タイムセールも続々登場 #今年最後の最後"
    ]:
        _text = CleanText(text).to_lower().to_adjust_line_code().to_remove_url().to_adjust_zero_number().to_adjust_mention().to_remove_symbol().text
        doc = nlp()(_text, disable=['ner'])

        other_texts = [token.lemma_ for token in doc]

        other_corpus = [dictionary.doc2bow(text) for text in [other_texts]]
        unseen_doc = other_corpus[0]
        vector = model[unseen_doc]

        vector = sorted(vector, key=lambda x: x[1], reverse=True)

        topic_id = vector[0][0] + 1
        ratio = vector[0][1]

        if topic_id == 1:
            print('ニュース', ratio, text)

        if topic_id == 2:
            print('ニュース(アイドル)', ratio, text)


