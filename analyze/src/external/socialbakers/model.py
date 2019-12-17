from dataclasses import dataclass


@dataclass
class TwitterData:

    # 計測月
    year: str
    # 計測月
    month: str
    # 平均フォロワー
    average_number_of_followers: str
    # 平均インタラクション
    average_number_of_interactions: str
    # リツイート率
    retweets_rate: str
    # いいね率
    likes: str
    # 返信率
    replies: str

    def __post_init__(self):
        def clean(_s: str):
            return _s.replace(" ", "").replace("	", "").replace("\n", "")

        self.year = clean(self.year)
        self.month = clean(self.month)
        self.average_number_of_followers = clean(self.average_number_of_followers)
        self.average_number_of_interactions = clean(self.average_number_of_interactions)
        self.retweets_rate = clean(self.retweets_rate)
        self.likes = clean(self.likes)
        self.replies = clean(self.replies)


MONTHLY_LIST = {
    "JANUARY": {
        "en": "january",
        "ja": "1月"
    },
    "FEBRUARY": {
        "en": "february",
        "ja": "2月"
    },
    "MARCH": {
        "en": "march",
        "ja": "3月"
    },
    "APRIL": {
        "en": "april",
        "ja": "4月"
    },
    "MAY": {
        "en": "may",
        "ja": "5月"
    },
    "JUNE": {
        "en": "june",
        "ja": "6月"
    },
    "JULY": {
        "en": "july",
        "ja": "7月"
    },
    "AUGUST": {
        "en": "august",
        "ja": "8月"
    },
    "SEPTEMBER": {
        "en": "september",
        "ja": "9月"
    },
    "OCTOBER": {
        "en": "october",
        "ja": "10月"
    },
    "NOVEMBER": {
        "en": "november",
        "ja": "11月"
    },
    "DECEMBER": {
        "en": "december",
        "ja": "12月"
    }
}
