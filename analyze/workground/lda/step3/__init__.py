import os
import sys
import json
import time
import glob
from pathlib import Path

import gensim
from gensim import corpora

from common import get_logger
from nlp.stopword import stop_words

logger = get_logger(__name__)


def extract(_docs):
    """名詞のみ抽出"""
    result = []
    for _doc in _docs:
        if _doc["tag"] == "名詞-普通名詞-一般" or \
                _doc["tag"] == "名詞-普通名詞-サ変可能" or \
                _doc["tag"] == "名詞-固有名詞-一般" or \
                _doc["tag"] == "名詞-固有名詞-地名-国":

            result.append(_doc.get("lemma", ""))
    return result


def get_save_train_data_path(path):
    base_path = Path(os.path.dirname(__file__))
    return str(base_path / "t-{}".format(str(path)))


def test(lda_model, test_corpus):
    import numpy as np

    N = sum(count for doc in test_corpus for id, count in doc)
    print("N: ",N)

    perplexity = np.exp2(-lda_model.log_perplexity(test_corpus))
    print("perplexity:", perplexity)


def run(path, topic_id=5):
    """トピックモデルの構築"""
    start_time = time.perf_counter()
    dictionary = corpora.Dictionary([])

    if not len(glob.glob(path)):
        logger.error("指定のファイルパスではjson形式のファイルは見つかりませんでした。  {} \nパスを確認してください。".format(path))
        sys.exit(1)

    nouns_list = []
    for p in glob.glob(path):
        logger.info("次のファイルから辞書を作成します。 {}".format(os.path.abspath(p)))
        with open(os.path.abspath(p)) as f:
            for line in f.readlines():
                docs = json.loads(line.replace("\n", ""))

                # 名詞と動詞が各一つ以上入っているものに限定
                words = extract(docs)
                if not len(words):
                    continue

                nouns = [word for word in words if word not in stop_words]
                # ゴミデータがあるので削除
                nouns = [n for n in nouns if n != " " and n != "️"]

                if len(nouns):
                    new_dictionary = corpora.Dictionary([nouns])
                    dictionary.merge_with(new_dictionary)
                    nouns_list.append(nouns)

    dictionary.filter_extremes(no_below=3, no_above=0.8)
    logger.info("辞書の作成が完了しました。")

    logger.info("コーパスの作成を開始します。")
    corpus = [dictionary.doc2bow(t) for t in nouns_list]
    logger.info("コーパスの作成を完了しました。")

    if len(nouns_list):
        logger.info("トピックモデルを構築します。")
        # モデルの作成
        dictionary.save(get_save_train_data_path("DICTIONARY"))
        corpora.MmCorpus.serialize(get_save_train_data_path("CORPUS_FILE_NAME"), corpus)

        print(dictionary)

        lda = gensim.models.ldamodel.LdaModel(
            corpus=corpus,
            num_topics=topic_id,
            id2word=dictionary
        )

        logger.info("トピックモデルの構築が完了しました。")

        logger.info("モデルを保存しています。")
        lda.save(get_save_train_data_path("Model"))
        # test(lda, test_corpus=corpus)
    else:
        logger.info("トピック解析対象のデータが存在しませんでした。")

    logger.info("処理時間: {}".format(time.perf_counter()-start_time))

