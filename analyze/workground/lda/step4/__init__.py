import math
import os
from pathlib import Path

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


def run(
    corpus_path="../step3/t-CORPUS_FILE_NAME",
    dictionary_path="../step3/t-DICTIONARY",
    model_path="../step3/t-Model",
    font_path=""
):
    """可視化・モデルの評価を行う"""
    logger.info("トピックモデルの評価・可視化を行います。")

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

    logger.info("ワードクラウドを作成します")
    fig, axs = plt.subplots(ncols=2, nrows=math.ceil(model.num_topics/2), figsize=(10,40))
    axs = axs.flatten()

    def color_func(word, font_size, position, orientation, random_state, font_path):
        return 'darkturquoise'

    for i, t in enumerate(range(model.num_topics)):

        x = dict(model.show_topic(t, 30))
        im = WordCloud(
            font_path=font_path,
            background_color='black',
            color_func=color_func,
            max_words=4000,
            width=300, height=300,
            random_state=0,
            scale=2
        ).generate_from_frequencies(x)
        axs[i].imshow(im.recolor(colormap='Paired_r', random_state=244), alpha=0.98)
        axs[i].axis('off')
        axs[i].set_title('Topic '+str(t + 1))

    # vis
    plt.tight_layout()
    # save as png
    plt.savefig(get_path('wordcloud.png'))
    logger.info("ワードクラウドを作成しました。")

    logger.info("LDAVizを作成します。")
    vis_pcoa = pyLDAvis.gensim.prepare(model, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis_pcoa, get_path('pyldavis_output_pcoa.html'))
    logger.info("LDAVizを作成しました。")
