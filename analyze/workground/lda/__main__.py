import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import fire

from lda.step1 import run as step1
from lda.step2 import run as step2
from lda.step3 import run as step3
from lda.step4 import run as step4

fire.Fire()

