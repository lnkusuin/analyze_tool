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
