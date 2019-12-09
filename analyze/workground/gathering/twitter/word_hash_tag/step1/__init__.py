from pathlib import Path
import os

from common import get_logger
from repository import FileRepository

from external.twitter.repository import TwitterRepository


logger = get_logger(__file__)


def get_path(path="output"):
    base_path = Path(os.path.dirname(__file__)).resolve()
    return str(base_path / path)


def run(word: str):
    """タイムライン情報取得コマンド"""

    logger.info("{}のワードを検索します。 ".format(word))
    twitter_repository = TwitterRepository()
    tweets = twitter_repository.get_all_tweets_by_word(30, **{
        "q": word
    })

    word = word.replace("#", 'hash_')
    FileRepository.save_json(get_path(), str(word), tweets)
    logger.info("{}のワードを検索しました。 件数{}件".format(word, len(tweets)))
