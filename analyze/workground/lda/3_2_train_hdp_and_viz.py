from builtins import print

import os

import setting
from setting import get_save_local_path

from context.lda.train import hdp_run

if __name__ == '__main__':
    # hdp_run(
    #     path=os.environ.get("CLASSIFY_TEXTS_PATH")
    # )

    from context.nlp import nlp

    a = nlp()("ありがとうございます")

    for _ in a:


        print({
            "text": _.text,
            "lemma": _.lemma_,
            "pos": _.pos_,
            "tag": _.tag_,
            "dep": _.dep_,
            "shape": _.shape_,
            "is_alpha": _.is_alpha,
            "is_stop": _.is_stop
        })
