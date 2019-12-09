import os
from pathlib import Path
import pickle

from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.dictionary import Dictionary

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
        model_path="../step3/t-Model-6"
        ):
    doc = nlp()(docs, disable=['ner'])
    texts, corpus, dictionary, model = load_state(texts_path, corpus_path, dictionary_path, model_path)

    other_texts = [token.lemma_ for token in doc]

    other_corpus = [dictionary.doc2bow(text) for text in [other_texts]]
    unseen_doc = other_corpus[0]
    vector = model[unseen_doc]

    vector = sorted(vector, key=lambda x: x[1], reverse=True)

    print(vector[0][0] + 1, vector[0][1])


