import functools
import os
import itertools

import matplotlib
matplotlib.font_manager._rebuild()
matplotlib.rcParams['font.family'] = 'IPAexGothic'

import pandas as pd

import setting

from common import get_logger
from context.lda.classify import run
from setting import get_save_local_path


logger = get_logger(__file__)


if __name__ == '__main__':
    results = []
    classify_dir_base = functools.partial(get_save_local_path, prefix="classify")()

    g = run(
        texts_path=os.environ.get("CLASSIFY_TEXTS_PATH"),
        corpus_path=os.environ.get("CLASSIFY_CORPUS_PATH"),
        dictionary_path=os.environ.get("CLASSIFY_DICTIONARY_PATH"),
        model_path=os.environ.get("CLASSIFY_MODEL_PATH"),
    )
    model = None
    for corpus, dictionary, model, text in g:
        results.append([
            text["topic_id"],
            text["ratio"],
            text["ratio_str"],
            " ".join(text["hash_tags"]),
            " ".join(text["words"]),
            text["text"]
        ])
        model = model

    df = pd.DataFrame(results, columns=["トピックid", "確率", "確率(s)", "ハッシュタグ", "ワード", "元テキスト", ])

    df = df.query("確率 >= 0.6")
    df = df.sort_values(by="トピックid")
    csv_path = classify_dir_base("classify_result.csv")
    df.to_csv(csv_path, index=False, encoding="utf_8_sig")
    logger.info("vd {}".format(csv_path))

    logger.info("既存テキストの振り分けを行いました。")

    hash_tags_list = []
    words_list = []

    for i, t in enumerate(range(model.num_topics)):
        topic_id = t+1

        filterd_item = [item for item in results if item[0] == (t+1)]

        _c = " ".join([item[3] for item in filterd_item]).split(" ")
        hash_tags = [_c for _c in _c if _c != ""]
        for hash_tag in hash_tags:
            hash_tags_list.append([topic_id, hash_tag])

        words = [item[4].split() for item in filterd_item]
        flatt_words = list(itertools.chain.from_iterable(words))
        for word in flatt_words:
            words_list.append([topic_id, word])

    pd.DataFrame(hash_tags_list, columns=["topic_id", "hash_tag"]).to_csv(classify_dir_base("hash_tags.csv"), index=False)
    pd.DataFrame(words_list, columns=["topic_id", "word"]).to_csv(classify_dir_base("words.csv"), index=False)

    logger.info("処理が完了しました。")
