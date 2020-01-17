import json
from pathlib import Path
from datetime import datetime

import pandas as pd

from common import get_logger

logger = get_logger(__file__)


class FileRepository:

    @classmethod
    def create_dir(cls, _dir, name):
        path = Path(_dir)
        if not path.exists():
            path.mkdir()

        path = path / str(str(name) + "_" + str(datetime.now().time()))
        if not path.exists():
            path.mkdir()

        return path

    @classmethod
    def save_json(cls, path, data):
        logger.info("{}にデータを書き込みます".format(path))

        with open(path, "w") as f:
            json.dump(data, f)

        logger.info("{}にデータ書き込みが完了しました。".format(path))

    @classmethod
    def load_json(self, path):
        logger.info("{}のデータを読み込みます".format(path))
        with open(path) as f:
            json_data = json.load(f)
            for item in json_data:
                yield item

        logger.info("{}のデータの読み込みが完了しました。".format(path))

    @classmethod
    def to_csv(cls, data, path):
        logger.info("{}にデータを書き込みます。".format(path))
        df = pd.DataFrame(data)
        df.to_csv(path, index=False)
        logger.info("{}にデータ書き込みが完了しました。".format(path))

