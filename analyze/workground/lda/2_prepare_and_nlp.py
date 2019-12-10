import os

import setting

from context.lda.prepare import run as prepare_run
from context.lda.nlp import run as nlp_run

if __name__ == '__main__':
    nlp_path = prepare_run(path=os.environ.get("PREPARED_PATH"))
    nlp_run(
        path=nlp_path,
        n_jobs=os.environ.get("NLP_N_JOBS"),
        batch_size=os.environ.get("NLP_BATCH_SIZE"),
    )

