import csv

import pandas as pd

from common import get_logger
from nlp import CleanText


logger = get_logger(__name__)


def run(path):
    """テキストデータの前処理"""

    logger.info("CSVファイルを読み込みます。")

    count = 0
    texts = []
    with open(path) as f:
        logger.info("CSVファイルの読み込みが完了しました。")
        reader = csv.DictReader(f)
        for item in reader:
            # リツイート省く
            if not item.get("text", "").startswith("RT "):
                texts.append(CleanText(item.get("text", "")).to_lower().to_adjust_line_code().to_remove_url().to_adjust_zero_number().to_adjust_mention().to_remove_symbol().text)
                count += 1
            if count % 10000 == 0:
                logger.info(count)

    path = './adjust.csv'
    print(len(texts))
    pd.DataFrame(texts).to_csv(path, index=False, header=["text"])

    return path
