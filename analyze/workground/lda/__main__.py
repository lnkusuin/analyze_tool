import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import fire


class Command:

    def step1(self, path):
        from lda.step1 import run
        return run(path)

    def step2(self, path, n_jobs=4, batch_size=1000):
        from lda.step2 import run
        return run(path, n_jobs=n_jobs, batch_size=batch_size)

    def step3(self, path, topic_id=5):
        from lda.step3 import run
        return run(path, topic_id=topic_id)

    def step4(self, font_path):
        from lda.step4 import run
        return run(font_path=font_path)



fire.Fire(Command)

