from external.google import build, get_google_credentials


def get_service():
    """Google Driveの参照を取得

    :return:
    """
    return build("drive", "v3", credentials=get_google_credentials())
