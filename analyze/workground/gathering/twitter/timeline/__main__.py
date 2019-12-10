import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../src'))

import fire

from prepare import run as step1

fire.Fire()

