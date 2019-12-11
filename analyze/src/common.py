import logging

log_path = "/tmp/analyzed_app.log"
print("see log {}".format(log_path))


def get_logger(name):
    """
    loggerの取得
    :return:
    """
    logging.basicConfig(
        format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
        filename=log_path
    )
    logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger
