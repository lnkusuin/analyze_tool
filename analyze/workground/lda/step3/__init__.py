import os
import sys
import json
import time
import glob
import pickle
import math
from pathlib import Path
from collections import defaultdict
from multiprocessing import Value

from joblib import Parallel, delayed
from tqdm import tqdm
import numpy as np
import pandas as pd
import gensim
from gensim import corpora
from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.dictionary import Dictionary
from wordcloud import WordCloud
import matplotlib
import matplotlib.pylab as plt
matplotlib.rcParams['font.family'] = 'AppleGothic'

import pyLDAvis
import pyLDAvis.gensim

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
                _doc["tag"] == "名詞-固有名詞-地名-国" or \
                _doc["tag"] == "形容詞-一般" or \
                _doc["pos"] == "VERB":

            result.append(_doc.get("lemma", ""))
    return result


def get_save_train_data_path(path):
    base_path = Path(os.path.dirname(__file__))
    return str(base_path / "t-{}".format(str(path)))


def create_word_cloud(model, font_path):
    logger.info("ワードクラウドを作成します(トピック数:{})".format(model.num_topics))
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
    plt.savefig(get_save_train_data_path('wordcloud{}.png'.format(model.num_topics)))
    logger.info("ワードクラウドを作成しました。(トピック数: {})".format(model.num_topics))


def create_viz(model, corpus, dictionary):
    # logger.info("LDAVizを作成します。")
    # vis_pcoa = pyLDAvis.gensim.prepare(model, corpus, dictionary, sort_topics=False)
    # pyLDAvis.save_html(vis_pcoa, get_path('pyldavis_output_pcoa.html'))
    # logger.info("LDAVizを作成しました。")

    # Vis t-SNE
    logger.info("t-SNEを作成します。(トピック数:{})".format(model.num_topics))
    vis_tsne = pyLDAvis.gensim.prepare(model, corpus, dictionary, mds='tsne', sort_topics=False)
    # save as html
    pyLDAvis.save_html(vis_tsne, get_save_train_data_path('pyldavis_output_tsne{}.html'.format(model.num_topics)))
    logger.info("t-SNEを作成します。(トピック数:{})".format(model.num_topics))


def evaluation(n_topic, texts, corpus, dictionary, font_path):

    passes = 20
    iterations = 400

    model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=n_topic,
        random_state=0,
        iterations=iterations,
        passes=passes
    )
    perplexity_vals = np.exp2(-model.log_perplexity(corpus))

    create_word_cloud(model, font_path)

    model.save(get_save_train_data_path("Model-{}".format(model.num_topics)))

    return model, n_topic, texts, corpus, dictionary, perplexity_vals


def evaluation2(model, corpus, dictionary):
    create_viz(model, corpus, dictionary)


def save_z(x_topics: list, perplexity_vals: list, coherence_vals: list):
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

def test(lda_model, test_corpus):
    import numpy as np

    N = sum(count for doc in test_corpus for id, count in doc)
    print("N: ", N)

    perplexity = np.exp2(-lda_model.log_perplexity(test_corpus))
    print("perplexity:", perplexity)


def run(path, font_path):
    """トピックモデルの構築・可視化・モデルの評価を行う"""
    start_time = time.perf_counter()
    dictionary = corpora.Dictionary([])

    if not len(glob.glob(path)):
        logger.error("指定のファイルパスではjson形式のファイルは見つかりませんでした。  {} \nパスを確認してください。".format(path))
        sys.exit(1)

    texts = []
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
                    texts.append(nouns)
    # setting frequency
    frequency = defaultdict(int)

    # count the number of occurrences of the word
    for text in texts:
        for token in text:
            frequency[token] += 1

    with open(get_save_train_data_path("TEXTS"), "wb") as f:
        pickle.dump(texts, f)

    dictionary.filter_extremes(no_below=3, no_above=0.1)
    logger.info("辞書の作成が完了しました。")

    logger.info("コーパスの作成を開始します。")
    corpus = [dictionary.doc2bow(t) for t in texts]
    # tfidf = gensim.models.TfidfModel(corpus)
    # tfidf.save('model.tfidf')
    # corpus = tfidf[corpus]

    logger.info("コーパスの作成を完了しました。")
    dictionary.save(get_save_train_data_path("DICTIONARY"))
    dictionary.save_as_text(get_save_train_data_path("DICTIONARY.txt"))
    corpora.MmCorpus.serialize(get_save_train_data_path("CORPUS_FILE_NAME"), corpus)

    if len(texts):
        start = 2
        limit = 30
        step = 2

        executor = Parallel(n_jobs=-1, verbose=10, backend="multiprocessing", prefer="processes")

        # トピックごとにモデル算出(並列処理)
        logger.info("トピックモデルの構築とワードクラウドの作成を行います。")
        d = []
        for n_topic in range(start, limit, step):
            d.append(delayed(evaluation)(n_topic, texts, corpus, dictionary, font_path))
        logger.info("トピックモデルの構築とワードクラウドの作成を行いました。")

        # トピックごとにcoherenceを算出(直列処理) 図の作成￿
        logger.info("トピック毎にcoherenceを算出し、評価グラフとして保存します。")
        x_topics = []
        perplexity_vals_list = []
        coherence_vals_list =[]
        d2 = []
        for model, n_topic, texts, corpus, dictionary, perplexity_vals in executor(d):
            coherence_model_lda = gensim.models.CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            x_topics.append(n_topic)
            perplexity_vals_list.append(perplexity_vals)
            coherence_vals_list.append(coherence_model_lda.get_coherence())

            save_z(x_topics, perplexity_vals_list, coherence_vals_list)

            d2.append(delayed(evaluation2)(model, corpus, dictionary))
        logger.info("トピック毎にcoherenceを算出し、評価グラフとして保存処理を完了します。")

        logger.info("t-sneを作成します。")
        executor(d2)
        logger.info("t-sneを作成しました。")

    else:
        logger.info("トピック解析対象のデータが存在しませんでした。")

    logger.info("処理時間: {}".format(time.perf_counter()-start_time))

