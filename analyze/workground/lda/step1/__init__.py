import os
import csv
import json
from pathlib import Path

import pandas as pd

from common import get_logger
from nlp import CleanText


logger = get_logger(__name__)


def get_base_path(name:str, path="output"):
    base_path = Path(os.path.dirname(__file__)).resolve()
    return str(base_path / path / name)


def open_json(path):
    with open(path) as f:
        items = json.load(f)
        for item in items:
            # リツイート以外
            text = item.get("text", "")
            if not text.startswith("RT "):
                yield text



def open_csv(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        for item in reader:
            # リツイート以外
            text = item.get("text", "")
            if not text.startswith("RT "):
                yield text


def run(path, type="csv"):
    """テキストデータの前処理"""
    logger.info("テキストの前処理を開始します。")
    count = 0
    texts = []
    _open = None

    if type == "json":
        _open = open_json
        logger.info("jsonファイルを読み込みます。")
    elif type == "csv":
        _open = open_csv
        logger.info("CSVファイルを読み込みます。")

    # リツイートが省かれている
    for text in _open(path):
        texts.append(CleanText(text).to_lower().to_adjust_line_code().to_remove_url().to_adjust_zero_number().to_adjust_mention().to_remove_symbol().text)
        count += 1

        if count % 10000 == 0:
            logger.info(count)

    print(len(texts))

    path = get_base_path("adjust.csv")
    pd.DataFrame(texts).to_csv(path, index=False, header=["text"], encoding="utf-8")

    logger.info("テキストの前処理を完了しました。")

    return path
