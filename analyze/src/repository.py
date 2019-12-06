import json
from pathlib import Path
from datetime import datetime

from common import get_logger

logger = get_logger(__file__)


class FileRepository:

    @classmethod
    def create_dir(cls, _dir, name):
        path = Path(_dir)
        if not path.exists():
            path.mkdir()

        path = path / str(name + "_" + str(datetime.now().time()))
        if not path.exists():
            path.mkdir()

        return path

    @classmethod
    def save_json(cls, _dir, name, data):
        path = cls.create_dir(_dir, name) / (name + ".json")
        logger.info("{}にデータを書き込みます".format(path))

        with open(path, "w") as f:
            json.dump(data, f)

        logger.info("{}にデータ書き込みが完了しました。".format(path))
