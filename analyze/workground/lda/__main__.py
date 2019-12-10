import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import fire

from prepare import run as prepare
from nlp_ import run as nlp
from learn import run as learn
# from step4 import run as step4
from classify import run as classify
from relearn import run as relearn


fire.Fire()

