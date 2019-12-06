"""
Googleサービスディスカバリー系の認証モジュール
"""
import os
from pathlib import Path

from dotenv import load_dotenv

import os.path
import pickle

from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request  # pylint: disable=no-name-in-module


# アプリケーション環境変数の読み込み
# ソースルートに.envファイルが存在すればその値を有線
BASE_PATH = Path(__file__).resolve().parent
env_file_path = BASE_PATH.joinpath(".env").resolve()
if os.path.exists(env_file_path):
    load_dotenv(dotenv_path=BASE_PATH.joinpath(".env").resolve())


def resolve_assets_path(path: str) -> str:
    """
    assetsディレクトリとパスの結合
    :param path:
    :return:
    """
    return BASE_PATH.joinpath("assets").joinpath(path)

CREDENTIAL_FILE_PATH = resolve_assets_path(os.getenv("CREDENTIAL_FILE"))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
    resolve_assets_path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
)

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    # 以下はgoogleドライブで必要なスコープ一覧
    "https://www.googleapis.com/auth/drive",
    # 以下はgoogleスプレッドシートで必要なスコープ一覧
    "https://www.googleapis.com/auth/spreadsheets",
    # 以下はGoogle Admin SDK で必要なスコープ一覧
    "https://www.googleapis.com/auth/admin.reports.audit.readonly",
]


def get_token_pickle() -> str:
    """
    認証情報の取得
    :return:
    """
    return resolve_assets_path("token.pickle")


def has_token_pickle() -> bool:
    """
    認証情報が作成されているか確認を行う
    :return:
    """
    return os.path.exists(resolve_assets_path("token.pickle"))


def get_google_credentials():
    """
    Google API関連のクレデンシャル情報の取得
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if has_token_pickle():
        with open(get_token_pickle(), "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIAL_FILE_PATH, SCOPES
            )
            flow.run_local_server()
        # Save the credentials for the next run
        with open(get_token_pickle(), "wb") as token:
            pickle.dump(creds, token)

    return creds
