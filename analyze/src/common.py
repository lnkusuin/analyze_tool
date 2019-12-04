import logging


def get_logger(name):
    """
    loggerの取得
    :return:
    """
    logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s"))

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    return logger


def logger_count(start_time, boundary=5000):
    incremental = boundary

    def _(count, end_time, logger):
        nonlocal start_time
        nonlocal boundary

        if count > boundary:
            logger.info(count)
            logger.info("経過時間: {}秒".format(end_time-start_time))
            boundary += incremental
    return _
