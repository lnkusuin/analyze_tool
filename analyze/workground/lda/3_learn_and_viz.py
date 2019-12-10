import os

import setting

from context.lda.train import run

if __name__ == '__main__':
    run(
        path=os.environ.get("TRAIN_PATH"),
        font_path=os.environ.get("FONT_PATH")
    )
