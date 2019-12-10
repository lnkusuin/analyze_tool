import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
