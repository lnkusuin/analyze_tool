import os
import csv
import json
from pathlib import Path

import pandas as pd

from common import get_logger
from context.nlp import CleanText


logger = get_logger(__name__)


def get_base_path(name:str, path="output"):
    base_path = Path(os.path.dirname(__file__)).resolve()
    return str(base_path / path / name)


def open_json(path):
    with open(path) as f:
        items = json.load(f)
        for item in items:
            # リツイート以外
            yield item.get("text", "")

def open_csv(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        for item in reader:
            text = item.get("text", "")
            yield text


def run(path, output_dir):
    """テキストデータの前処理"""
    logger.info("====テキストの前処理を開始します。====")
    count = 0
    texts = []
    _open = None

    root, ext = os.path.splitext(path)

    if ext == ".json":
        _open = open_json
        logger.info("jsonファイルを読み込みます。")
    elif ext == ".csv":
        _open = open_csv
        logger.info("CSVファイルを読み込みます。")

    # リツイートが省かれている
    for text in _open(path):
        texts.append(CleanText(text).to_lower().to_adjust_line_code().to_remove_url().to_adjust_zero_number().to_adjust_mention().to_remove_symbol().text)
        count += 1

        if count % 10000 == 0:
            logger.info(count)

    logger.info("対象テキスト数: {}".format(len(texts)))

    path = output_dir("prepare")("adjust.csv")
    pd.DataFrame(texts).to_csv(path, index=False, header=["text"], encoding="utf-8")
    logger.info("解析結果を以下に保存しました。 {}".format(path))

    logger.info("====テキストの前処理を完了しました。====")

    return path
