import os
import pickle
from pathlib import Path

import gensim
from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.dictionary import Dictionary

from common import get_logger

logger = get_logger(__file__)


def get_path(base, path):
    base_path = Path(os.path.dirname(base))
    return str(base_path / path)


def extract(_docs):
    """名詞のみ抽出"""
    result = []
    for _doc in _docs:
        if _doc["tag"] == "名詞-普通名詞-一般" or \
                _doc["tag"] == "名詞-普通名詞-サ変可能" or \
                _doc["tag"] == "名詞-固有名詞-一般" or \
                _doc["tag"] == "名詞-固有名詞-地名-国" or \
                _doc["tag"] == "形容詞-一般" or \
                _doc["pos"] == "VERB":

            result.append(_doc.get("lemma", ""))
    return result


def load_state(text_path, corpus_path, dictionary_path, model_path):
    """状態の復元"""

    logger.info("テキストを読み込みます")
    with open(text_path, "rb") as f:
        texts = pickle.load(f)

    logger.info("テキストの読み込みが完了しました。")

    logger.info("コーパスを読み込みます。")
    corpus = MmCorpus(corpus_path)
    # tfidf = gensim.models.TfidfModel(corpus)
    # corpus = tfidf[corpus]
    logger.info("コーパスの読み込みが完了しました。")

    logger.info("辞書を読み込みます。")
    dictionary = Dictionary.load(dictionary_path)
    logger.info("辞書の読み込みが完了しました。")

    logger.info("LDAを読み込みます。")
    model = gensim.models.ldamodel.LdaModel.load(model_path)
    logger.info("LDAの読み込みが完了しました。")

    return texts, corpus, dictionary, model


def save_evaluation_png(x_topics: list, perplexity_vals: list, coherence_vals: list):
    import matplotlib
    import matplotlib.pylab as plt
    matplotlib.rcParams['font.family'] = 'AppleGothic'

    fig, ax1 = plt.subplots(figsize=(12, 5))

    c1 = 'darkturquoise'
    ax1.plot(x_topics, coherence_vals, 'o-', color=c1)
    ax1.set_xlabel('Num Topics')
    ax1.set_ylabel('Coherence', color=c1)
    ax1.tick_params('y', colors=c1)

    c2 = 'slategray'
    ax2 = ax1.twinx()
    ax2.plot(x_topics, perplexity_vals, 'o-', color=c2)
    ax2.set_ylabel('Perplexity', color=c2)
    ax2.tick_params('y', colors=c2)

    ax1.set_xticks(x_topics)
    fig.tight_layout()
    plt.savefig(get_save_train_data_path('evaluation.png'))
