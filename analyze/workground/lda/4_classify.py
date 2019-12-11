import functools
import os

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
    for corpus, dictionary, model, text in g:
        results.append([
            text["topic_id"],
            text["ratio"],
            text["ratio_str"],
            " ".join(text["hash_tags"]),
            " ".join(text["words"]),
            text["text"]
        ])

    df = pd.DataFrame(results, columns=["トピックid", "確率", "確率(s)", "ハッシュタグ", "ワード", "元テキスト", ])

    df = df.query("確率 >= 0.6")
    df = df.sort_values(by="トピックid")
    df.to_csv(classify_dir_base("classify_result.csv"), index=False, encoding="utf_8_sig")

    logger.info("既存テキストの振り分けを行いました。")
    #
    # df.to_csv("aaa_2.csv")
    #
    # # テキスト1
    # df1 = df.query("~(トピック名=='不明1')")
    # df1 = df1.query("~(トピック名=='不明2')")
    # df1 = df1.query("確率 >= 0.6")
    # df1_words = df1["ワード"].values.tolist()
    # df1_words = list(map(lambda x: x.split(" "), df1_words))
    # with open("df1_words", "wb") as f:
    #     pickle.dump(df1_words, f)
    #
    # df1.to_csv("df1.csv")
    #
    # # テキスト2
    # df2 = df.query("トピック名=='不明1' | トピック名=='不明2'")
    # df2_words = df2["ワード"].values.tolist()
    # df2_words = list(map(lambda x: x.split(" "), df2_words))
    # with open("df2_words", "wb") as f:
    #     pickle.dump(df2_words, f)
    #
    # df2.to_csv("df2.csv")
