import pickle

import gensim
from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.dictionary import Dictionary


from common import get_logger

logger = get_logger(__file__)


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