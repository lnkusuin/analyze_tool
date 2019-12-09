import os
import json

from requests_oauthlib import OAuth1Session

import external.twitter as module
from external.twitter.common import get_logger, sleep


logger = get_logger(__name__)


class BaseLocalRepository:

    @staticmethod
    def save_to_json(data, path):
        with open(path, "w") as f:
            json.dump(data, f)

    @staticmethod
    def load_from_json(path):
        with open(path) as f:
            json_data = json.load(f)
            for item in json_data:
                yield item


class Exception401(Exception):
    def __init__(self, message="", errors=""):

        super().__init__(message)

        self.errors = errors


class TwitterRepository:

    session = None

    def __init__(self):
        self.session = self.get_session()

    def get_session(self):
        return OAuth1Session(
            module.TWITTER_CONSUMER_KEY,
            module.TWITTER_CONSUMER_SECRET,
            module.TWITTER_ACCESS_TOKEN_KEY,
            module.TWITTER_ACCESS_TOKEN_SECRET
        )

    def _after_response(self, res):
        if res.status_code == 401:
            logger.info(res.text)

            return [], res.status_code

        if res.status_code != 200:
            return [], res.status_code

        return json.loads(res.text), res.status_code

    def save_retweets_info(self):
        """
        リツイート情報の保存
        :return:
        """
        pass

    def get_user_timeline(self, screen_name):
        res = self.session.get(
            "https://api.twitter.com/1.1/statuses/user_timeline.json",
            params={"screen_name": screen_name, "count": 200},
        )

        return self._after_response(res)

    def get_user_timeline_by_user_id(self, max_id: str="", **params):
        while True:
            try:
                params = {**params, "count": 200}
                if max_id:
                    params["max_id"] = max_id

                res = self.session.get(
                    "https://api.twitter.com/1.1/statuses/user_timeline.json",
                    params=params,
                )

                return self._after_response(res)
            except Exception as e:
                logger.info("get_user_timeline_by_user_idでコネクションエラー")
                sleep(10)
                self.session = self.get_session()

    def get_user_timeline_by_user_id_all(self, max_count, **params):

        count = 0
        max_id = ""
        results = []
        while True:
            logger.info("リクエスト{}回目".format(count + 1))
            ret, status = self.get_user_timeline_by_user_id(max_id, **params)

            if status == 429:
                logger.info("API制限となりました。15分秒遅延します。")
                sleep((60 * 15) + 30)
                continue

            if max_id == ret[-1]["id_str"]:
                break

            max_id = ret[-1]["id_str"]
            results.extend(ret)
            count = count + 1

            if count > max_count:
                break

        return results

    def get_tweets_by_word(self, next_results: str, **params):
        while True:
            try:
                if next_results:
                    res = self.session.get("https://api.twitter.com/1.1/search/tweets.json{}".format(next_results))
                else:
                    params = {
                        **params,
                        "count": 100,
                        "lang": "ja",
                        "locale": "ja",
                        "result_type": "recent"
                    }
                    res = self.session.get(
                        "https://api.twitter.com/1.1/search/tweets.json",
                        params=params,
                    )

                return self._after_response(res)
            except Exception as e:
                logger.info("get_tweets_by_wordでコネクションエラー")
                sleep(10)
                self.session = self.get_session()

    def get_all_tweets_by_word(self, max_count: int, **params):
        count = 0
        results = []
        next_results = ""

        while True:
            logger.info("リクエスト{}回目".format(count + 1))
            ret, status = self.get_tweets_by_word(next_results, **params)

            statuses = ret['statuses']
            search_metadata = ret['search_metadata']
            next_results = search_metadata["next_results"]

            if status == 429:
                logger.info("API制限となりました。15分秒遅延します。")
                sleep((60 * 15) + 30)
                continue

            if not len(statuses):
                break

            results.extend(statuses)
            count = count + 1

            if count > max_count:
                break

        return results

    def get_followers_user_ids(self, screen_name, next_cursor_str=-1):
        """
        対象screen_nameでのフォローワーのidリストを取得する
        :param screen_name:
        :param next_cursor_str:
        :return:
        """
        while True:
            try:
                res = self.session.get(
                    "https://api.twitter.com/1.1/followers/ids.json",
                    params={
                        "screen_name": screen_name,
                        "count": 5000,
                        "cursor": next_cursor_str,
                    },
                )
                return self._after_response(res)
            except Exception as e:
                logger.info("get_followers_user_idsでコネクションエラー")
                sleep(10)
                self.session = self.get_session()

    def rate_limit_status(self):
        """
        API制限のステータス確認API
        :return:
        """
        res = self.session.get(
            "https://api.twitter.com/1.1/application/rate_limit_status.json"
        )

        return self._after_response(res)

    @staticmethod
    def wait_limit(status_code: int, delay_time=(60 * 15) + 30):
        if status_code == 429:
            logger.info("API制限となりました。15分30秒遅延します。")
            sleep(delay_time)
