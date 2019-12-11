import os
import setting

from common import get_logger
from repository import FileRepository

from external.twitter.repository import TwitterRepository

from setting import get_save_local_path

logger = get_logger(__file__)


if __name__ == '__main__':
    """タイムライン情報取得コマンド"""
    word = os.environ.get("WORD")

    logger.info("{}のワードを検索します。 ".format(word))
    print(word)
    twitter_repository = TwitterRepository()
    tweets = twitter_repository.get_all_tweets_by_word(100, **{
        "q": word
    })

    word = word.replace("#", 'hash_')
    FileRepository.save_json(get_save_local_path(prefix="gathering")(word + ".json"), tweets)
    logger.info("{}のワードを検索しました。 件数{}件".format(word, len(tweets)))
