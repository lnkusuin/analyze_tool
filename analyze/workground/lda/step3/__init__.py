import os
import sys
import time
import glob

import gensim
from gensim import corpora
import pandas as pd

from common import get_logger
from stopword import stop_words

logger = get_logger(__name__)


def run(path):
    """トピックモデルの構築"""
    start_time = time.perf_counter()
    dictionary = corpora.Dictionary([])
    corpus = []

    for p in glob.glob(path):
        logger.info("次のファイルを読み込みます {}".format(os.path.abspath(p)))
        with open(os.path.abspath(p)) as f:
            for line in f.readlines():
                nouns = line.replace("\n", "").split(",")
                nouns = [word for word in nouns if word not in stop_words]

                if len(nouns):
                    new_dictionary = corpora.Dictionary([line.split(",")])
                    dictionary.merge_with(new_dictionary)
                    corpus.extend([dictionary.doc2bow(nouns)])

    logger.info("辞書の作成が完了しました。")
    logger.info("トピックモデルを構築します。")
    # モデルの作成
    dictionary.save("./DICT_FILE_NAME")
    corpora.MmCorpus.serialize("./CORPUS_FILE_NAME", corpus)

    print(dictionary)

    lda = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        num_topics=10,
        id2word=dictionary
    )

    logger.info("トピックモデルの構築が完了しました。")
    import pprint
    pprint.pprint(lda.show_topics())
    lda.save("LDA_MODEL_FILE_NAME")

    logger.info("最終結果をファイルに保存します。")
    data = []
    for item in lda.show_topics():
        for _item in item[1].split('+'):
            score = _item.split("*")[0]
            label = _item.split("*")[1]
            data.append([item[0], score.replace('"', ""), label.replace('"', "")])

    df = pd.DataFrame(data)
    df.to_csv("res.csv", index=False, header=["topic", 'score', 'label'])

    logger.info("処理時間: {}".format(time.perf_counter()-start_time))
