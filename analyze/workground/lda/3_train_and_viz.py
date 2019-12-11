import os

import setting
from setting import get_save_local_path

from context.lda.train import run

if __name__ == '__main__':
    run(
        path=os.environ.get("TRAIN_PATH"),
        font_path=os.environ.get("FONT_PATH"),
        dir_base=get_save_local_path
    )
