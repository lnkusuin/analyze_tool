import os
import sys
import json
import time
import glob

import gensim
from gensim import corpora
import pandas as pd

from common import get_logger
from stopword import stop_words

logger = get_logger(__name__)


def extract(_docs):

    result = []
    for _doc in _docs:
        if _doc["tag"] == "名詞-普通名詞-一般" or \
                _doc["tag"] == "名詞-普通名詞-サ変可能" or \
                _doc["tag"] == "名詞-固有名詞-一般" or \
                _doc["tag"] == "名詞-固有名詞-地名-国" or \
                _doc["pos"] == "VERB":
            result.append(_doc.get("lemma", ""))

    return result


def run(path):
    """トピックモデルの構築"""
    start_time = time.perf_counter()
    dictionary = corpora.Dictionary([])
    corpus = []

    if not len(glob.glob(path)):
        logger.error("指定のファイルパスではjson形式のファイルは見つかりませんでした。  {}".format(path))
        sys.exit(1)

    ff = open("tmp.txt", "w")
    nouns = []
    for p in glob.glob(path):
        logger.info("次のファイルを読み込みます {}".format(os.path.abspath(p)))
        with open(os.path.abspath(p)) as f:
            for line in f.readlines():
                docs = json.loads(line.replace("\n", ""))

                #json.dump(docs, ff, ensure_ascii=False, indent=2)

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
                    corpus.extend([dictionary.doc2bow(nouns)])

    logger.info("辞書の作成が完了しました。")

    if len(nouns):
        logger.info("トピックモデルを構築します。")
        # モデルの作成
        # dictionary.save("./DICT_FILE_NAME")
        # corpora.MmCorpus.serialize("./CORPUS_FILE_NAME", corpus)

        print(dictionary)

        lda = gensim.models.ldamodel.LdaModel(
            corpus=corpus,
            num_topics=5,
            id2word=dictionary
        )

        logger.info("トピックモデルの構築が完了しました。")
        import pprint
        pprint.pprint(lda.show_topics())
        # lda.save("LDA_MODEL_FILE_NAME")

        logger.info("最終結果をファイルに保存します。")
        data = []
        for item in lda.show_topics():
            for _item in item[1].split('+'):
                score = _item.split("*")[0]
                label = _item.split("*")[1]
                data.append([item[0], score.replace('"', ""), label.replace('"', "")])

        df = pd.DataFrame(data)
        df.to_csv("res.csv", index=False, header=["topic", 'score', 'label'])
    else:
        logger.info("トピック解析対象のデータが存在しませんでした。")

    logger.info("処理時間: {}".format(time.perf_counter()-start_time))
