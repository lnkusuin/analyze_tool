from builtins import print

import os

import setting
from setting import get_save_local_path

from context.lda.train import hdp_run

if __name__ == '__main__':
    hdp_run(
        path=os.environ.get("TRAIN_PATH")
    )
