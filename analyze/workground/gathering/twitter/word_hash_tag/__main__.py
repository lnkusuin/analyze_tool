import sys
import os

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../src'))

import fire

from step1 import run as step1

fire.Fire()

