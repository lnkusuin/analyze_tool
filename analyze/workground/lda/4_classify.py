import functools
import os

from wordcloud import WordCloud
import matplotlib
import matplotlib.pylab as plt
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
    df.to_csv(classify_dir_base("classify_result.csv"), index=False, encoding="utf_8_sig")

    logger.info("既存テキストの振り分けを行いました。")


    import math
    logger.info("ワードクラウドを作成します(トピック数:{})".format(model.num_topics))
    fig, axs = plt.subplots(ncols=1, nrows=model.num_topics, figsize=(10, 40))
    axs = axs.flatten()

    def color_func(word, font_size, position, orientation, random_state, font_path):
        return 'darkturquoise'

    from collections import Counter

    for i, t in enumerate(range(model.num_topics)):
        filterd_item = [item for item in results if item[0] == (t+1)]

        _c = " ".join([item[3] for item in filterd_item]).split(" ")
        _c = [_c for _c in _c if _c != ""]
        label = ""
        for l in Counter(_c).most_common(3):
            label += " #{} ".format(l[0])

        im = WordCloud(
            font_path='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc',
            background_color='black',
            color_func=color_func,
            width=700, height=300,
            random_state=0,
            scale=2
        ).generate(" ".join([item[4] for item in filterd_item]))

        print(label)
        axs[i].imshow(im.recolor(colormap='Paired_r', random_state=244), alpha=0.98)
        axs[i].axis('off')
        axs[i].set_title(label, fontsize=10)

    # vis
    plt.tight_layout()
    # save as png
    plt.savefig(classify_dir_base('wordcloud{}.png'.format(model.num_topics)))
    logger.info("処理が完了しました。")

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
