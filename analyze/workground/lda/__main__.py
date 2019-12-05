import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import fire
from lda.step1 import run as step1
from lda.step2 import run as step2
from lda.step3 import run as step3


def main(path: str = "", step_id: int = 0, n_jobs=4, batch_size=1000):
    # FIXME 抽象化するかも
    step_list = {1: step1, 2: step2, 3: step3}

    if step_id == 1:
        step1(path)
    elif step_id == 2:
        step2(path, n_jobs=n_jobs, batch_size=batch_size)
    elif step_id == 2:
        step3(path)
    else:
        pass
        # TODO すべて実行

    return ""


fire.Fire(main)

