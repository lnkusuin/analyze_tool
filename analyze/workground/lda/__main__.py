import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import fire
from lda.step1 import run as step1
from lda.step2 import run as step2
from lda.step3 import run as step3
from lda.step4 import run as step4


def main(path: str = "", step_id: int = 0, n_jobs=4, batch_size=1000, topic_id=5, font_path=""):
    """コマンドラインツール"""

    # FIXME 抽象化するかも サブコマンド管理でいいかもしれない
    step_list = {1: step1, 2: step2, 3: step3, 4: step4}

    # テキストデータの前処理
    if step_id == 1:
        step1(path)
    # 自然言語処理
    elif step_id == 2:
        step2(path, n_jobs=n_jobs, batch_size=batch_size)
    # トピックモデルの学習とモデルの評価
    elif step_id == 3:
        step3(path, topic_id=topic_id)
    # 可視化
    elif step_id == 4:
        step4(font_path=font_path)
    else:
        pass
        # TODO すべて実行

    return ""


fire.Fire(main)

