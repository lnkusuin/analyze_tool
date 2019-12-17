from pathlib import Path
from urllib import request
from dataclasses import asdict

import pandas as pd
from bs4 import BeautifulSoup
from common import get_logger
from external.socialbakers.model import TwitterData

logger = get_logger(__name__)


class LocalRepository:

    @staticmethod
    def save_to_csv(twitter_data: TwitterData, output_dir):
        file_name = 'social_bakers_twitter_{}_{}.csv'.format(twitter_data.year, twitter_data.month)
        csv_save_path = Path(output_dir) / file_name
        logger.info("データをCSVに保存します。 {}".format(file_name))
        pd.DataFrame([asdict(x) for x in [twitter_data]]). \
            to_csv(csv_save_path,
                   index=False,
                   header=["年", "月", "平均フォロワー", "平均インタラクション", "リツイート率", "いいね率", "返信率"])


class SocialBakersRepository:

    @staticmethod
    def scraping_from_japan_report_of_twitter_by_monthly(monthly: dict, year: str = "2019"):
        url = "https://www.socialbakers.com/resources/reports/japan/{}/{}".format(year, monthly["en"])
        logger.info("次のツイッタープラットフォームの情報を取得します。 {}".format(url))

        html = request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        def get_text(selector, d=""):
            try:
                return soup.select_one(selector).text
            except AttributeError as e:
                print(e)
                return d

        return TwitterData(
            year=year,
            month=monthly["ja"],
            average_number_of_followers=get_text(".average_number__fans > ul > li.gray.tw > p > strong"),
            average_number_of_interactions=get_text(".average_number__interactions > ul > li.gray.tw > p > strong"),
            retweets_rate=get_text("table > tbody > tr:nth-child(1) > td:nth-child(2)"),
            likes=get_text("table > tbody > tr.even.no-border > td:nth-child(2)"),
            replies=get_text("table > tbody > tr:nth-child(3) > td:nth-child(2)"),
        )
