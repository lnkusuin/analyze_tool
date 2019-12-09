import math
import os
import pickle
from pathlib import Path

from tqdm import tqdm
import numpy as np
import pandas as pd
import gensim
from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.dictionary import Dictionary
from wordcloud import WordCloud
import matplotlib
import matplotlib.pylab as plt
matplotlib.rcParams['font.family'] = 'AppleGothic'

import pyLDAvis
import pyLDAvis.gensim

from common import get_logger

logger = get_logger(__file__)


def load_file(path):
    """ファイルの読み込み"""
    path = get_path(path)

    with open(path) as f:
        return f.read()


def get_path(path):
    base_path = Path(os.path.dirname(__file__))
    return str(base_path / path)


def output_to_csv(model):
    data = []

    from pprint import pprint
    pprint(model.show_topics(num_words=30, num_topics=30))

    for item in model.show_topics(num_words=30):
        for _item in item[1].split('+'):
            score = _item.split("*")[0]
            label = _item.split("*")[1]
            data.append([item[0], score.replace('"', ""), label.replace('"', "")])

    df = pd.DataFrame(data)
    df.to_csv(get_path("res.csv"), index=False, header=["topic", 'score', 'label'])


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

    logger.info("CSVファイルに結果を出力します。'")
    output_to_csv(model)
    logger.info("CSVファイルへの出力が完了しました。")

    return texts, corpus, dictionary, model


def run(
    texts_path="../step3/t-TEXTS",
    corpus_path="../step3/t-CORPUS_FILE_NAME",
    dictionary_path="../step3/t-DICTIONARY",
    model_path="../step3/t-Model",
    font_path=""
):
    """モデルの生成"""
    logger.info("トピックモデルの評価・可視化を行います。")

    texts, corpus, dictionary, model = load_state(texts_path, corpus_path, dictionary_path, model_path)


