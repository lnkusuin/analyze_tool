from pathlib import Path
import os

import setting

from common import get_logger
from repository import FileRepository
from external.twitter.repository import TwitterRepository


logger = get_logger(__file__)


def get_path(path="output"):
    base_path = Path(os.path.dirname(__file__)).resolve()
    return str(base_path / path)


if __name__ == '__main__':
    """タイムライン情報取得コマンド"""
    word = os.environ.get("SEARCH_WORD")

    logger.info("{}のワードを検索します。 ".format(word))
    twitter_repository = TwitterRepository()
    tweets = twitter_repository.get_all_tweets_by_word(500, **{
        "q": word
    })

    word = word.replace("#", 'hash_')
    FileRepository.save_json(str(word) +'.json', tweets)
    logger.info("{}のワードを検索しました。 件数{}件".format(word, len(tweets)))

