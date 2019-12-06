import time

from tableauserverclient.server import ProjectItem, WorkbookItem

from common import get_logger
import external.tableau as settings
from external.tableau.repository import TableauTwitterRepository, get_auth

logger = get_logger(__file__)


class TableauTwitterService:
    """ タブローオンライン上にツイッター解析用の諸々サービスクラス"""

    @classmethod
    def prepare_workbook_area(cls, email: str) -> str:
        """タブローオンライン上に専用のワークブックエリアを作成する

        :param cls:
        :param email:
        :return: コンテンツのURL
        """
        logger.info("email: {}".format(email))

        project_item: ProjectItem = TableauTwitterRepository.create_project(
            project_name=email, parent_id=settings.TABLEAU_PUBLISH_BASE_PROJECT_ID
        )

        workbook_item: WorkbookItem = TableauTwitterRepository.publish_workbook(
            project_id=project_item.id,
            workbook_path=settings.MODULE_ROOT_PATH
            / "context/tableau/assets/z_twitter.twbx",
            file_name=str(time.time()),
        )

        # 生成URL例
        # https://10az.online.tableau.com/#/site/{content_url}/views/1574847027_456733/sheets/sheet0
        content_url = ""
        url = "{}/#/site/{}/views/{}".format(
            get_auth()[1].server_address,
            content_url,
            workbook_item.views[0].content_url.split("/")[0] + "/README",
        )

        logger.info("生成したURL: {}".format(url))
        return url

