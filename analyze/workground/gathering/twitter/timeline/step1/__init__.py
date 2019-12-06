from pathlib import Path
import os

from common import get_logger
from repository import FileRepository

from external.twitter.repository import TwitterRepository


logger = get_logger(__file__)


def get_path(path="output"):
    base_path = Path(os.path.dirname(__file__)).resolve()
    return str(base_path / path)


def run(screen_id: str):
    """タイムライン情報取得コマンド"""

    logger.info("{}のタイムライン情報を取得します。".format(screen_id))
    twitter_repository = TwitterRepository()
    time_lines = twitter_repository.get_user_timeline_by_user_id_all(screen_id)

    FileRepository.save_json(get_path(), str(screen_id), time_lines)
    logger.info("{}のタイムライン情報を取得しました。".format(screen_id))
