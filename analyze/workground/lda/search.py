import pandas as pd
from pprint import pprint

from common import get_logger

logger = get_logger(__file__)

pd.set_option("display.max_rows", 101)

if __name__ == '__main__':
    logger.info("")
    path = ""
    df = pd.read_csv(path)

    ret = df[df['text'].str.contains('コーラ')]


    pprint(len(ret))
    pprint(ret)


