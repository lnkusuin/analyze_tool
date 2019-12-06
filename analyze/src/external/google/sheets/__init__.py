from external.google import build, get_google_credentials


def get_service():
    """Google Sheetsの参照を取得
    :return:
    """
    return build("sheets", "v4", credentials=get_google_credentials())
