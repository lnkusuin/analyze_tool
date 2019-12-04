import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import fire
from lda.step1 import run as step1
from lda.step2 import run as step2
from lda.step3 import run as step3


def main(path: str = "", step_id: int = 0):
    step_list = {1: step1, 2: step2, 3: step3}

    if step_id in step_list:
        step = step_list[step_id]
        step(path)
    else:
        pass
        # TODO すべて実行

    return ""


fire.Fire(main)

