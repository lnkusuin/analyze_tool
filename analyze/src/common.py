import logging


def get_logger(name):
    """
    loggerの取得
    :return:
    """
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(name)s:%(message)s")
    logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger
