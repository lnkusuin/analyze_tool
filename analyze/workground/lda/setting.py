import os
import sys
from os.path import join, dirname
from datetime import datetime

from dotenv import load_dotenv

# FIXME パスを調整する必要あり
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def get_save_local_path(prefix=""):
    path = os.path.dirname(__file__) + "/output"
    if not os.path.exists(path):
        os.mkdir(path)

    prefix = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "_" + prefix
    path = path + "/" + prefix
    if not os.path.exists(path):
        os.mkdir(path)

    def _(name=""):
        if name:
            return path + "/" + name

        return path

    return _
