import time
import os
import sys
from pathlib import Path
from functools import partial
import shutil
import json

from joblib import Parallel, delayed
from spacy.util import minibatch
import pandas as pd

from common import get_logger
from nlp import nlp

logger = get_logger(__name__)


def process_nlp(batch_id, texts, output_dir, size):
    start_time = time.perf_counter()
    out_path = Path(os.path.dirname(__file__)) / output_dir / ("%d.json" % batch_id)
    if out_path.exists():
        return None

    logger.info("Processing batch {}".format(batch_id))
    with out_path.open("w", encoding="utf8") as f:
        for doc in nlp().pipe(texts, disable=['ner']):
            words = [{
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dep": token.dep_,
                "shape": token.shape_,
                "is_alpha": token.is_alpha,
                "is_stop": token.is_stop
            } for token in doc]
            f.write(json.dumps(words))
            f.write("\n")

    logger.info("Saved {} texts to {}.txt = ファイル総数:{} 単一の処理時間: {}".format(len(texts), batch_id, size, time.perf_counter() - start_time))


def run(path, n_jobs=4, batch_size=1000):
    """ 自然言語解析"""
    start_time = time.perf_counter()
    logger.info("辞書の作成を行います。")

    if not Path(path).exists():
        logger.error("指定のパスが見つかりませんでした。 {}".format(path))
        sys.exit(1)

    df = pd.read_csv(path)
    df = df.dropna(how='all')
    docs = df['text'].tolist()
    output_dir = "./output"
    p = Path(os.path.dirname(__file__)) / output_dir

    if p.exists():
        shutil.rmtree(p, ignore_errors=True)
        p.mkdir()

    partitions = minibatch(docs, size=batch_size)
    executor = Parallel(n_jobs=n_jobs, verbose=10, backend="multiprocessing", prefer="processes")
    do = delayed(partial(process_nlp, size=len(docs)/batch_size))
    tasks = (do(i, batch, output_dir) for i, batch in enumerate(partitions))
    executor(tasks)
