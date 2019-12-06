from context.dataprep.twitter.common import is_holiday


def test_is_holiday():
    """
    祝日判定を確認
    :return:
    """
    from datetime import datetime

    # 祝日であることを確認する

    holiday_data = [
        "2019-1-01",
        "2019-1-14",
        "2019-2-11",
        "2019-3-21",
        "2019-4-29",
        "2019-4-30",
        "2019-5-01",
        "2019-5-02",
        "2019-5-03",
        "2019-5-04",
        "2019-5-05",
        "2019-5-06",
        "2019-7-15",
        "2019-8-11",
        "2019-8-12",
        "2019-9-16",
        "2019-9-23",
        "2019-10-14",
        "2019-10-22",
        "2019-11-03",
        "2019-11-04",
        "2019-11-23",
    ]

    for day in holiday_data:
        assert 1 == is_holiday(datetime.strptime(day, "%Y-%m-%d").date())
