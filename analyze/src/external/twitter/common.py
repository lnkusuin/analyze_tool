"""
Twitter 解析モジュールの汎用処理置き場
"""

import logging
import time
import os
from datetime import datetime, timedelta, timezone
from dateutil import parser
from pathlib import Path

import jpholiday

logger = logging.getLogger(__name__)


def debug(data):
    """
    デバッグ用関数
    :param data:
    :return:
    """
    import pprint

    pprint.pprint(data, indent=4, width=4)


def sleep(_time: float, message: str = "") -> int:
    """
    遅延処理
    :param _time:
    :return _time:
    """
    logger.info("遅延{}秒 {}".format(_time, message))
    time.sleep(_time)

    return _time


def is_holiday(date):
    """
    祝日判定
    :param date:
    :return:
    """
    if date.weekday() >= 5 or jpholiday.is_holiday(date):
        return 1
    else:
        return 0


def convert_from_utc_to_jst(utc_date: str) -> datetime:
    """
    jst時刻からutc時刻に変換
    :param utc_date:
    :return:
    """
    return parser.parse(utc_date).astimezone(timezone(timedelta(hours=+9), "JST"))


def get_assets_path(path):
    """
    アセットのパスを取得
    :param path:
    :return:
    """
    return Path(__file__).resolve().parent / "assets" / path


def init_file(save_path: str) -> str:
    """
    ファイル作成の初期化
    :param save_path:
    :return:
    """
    save_path = get_assets_path(save_path)
    if os.path.exists(save_path):
        os.remove(save_path)

    return save_path


def get_logger(name):
    """
    loggerの取得
    :return:
    """
    logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s:%(asctime)s:%(name)s:%(message)s"
    )

    root = logging.getLogger(name)
    root.setLevel(logging.INFO)
    return root


class LoggerHelper:

    message: str = ""
    logger = None

    def __init__(self, name, message):
        self.message = message
        self.logger = get_logger(name)

    def start(self):
        self.logger.info("----------{}を開始します----------".format(self.message))

        return self

    def end(self):
        self.logger.info("----------{}を完了します----------".format(self.message))

        return self

    def print(self, message):
        self.logger.info(message)

    def start_time(self):
        self.logger.info("開始時間 {}".format(datetime.now()))

    def end_time(self):
        self.logger.info("終了時間 {}".format(datetime.now()))
