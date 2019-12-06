import pytest

import external.tableau as settings
from external.tableau.repository import TableauTwitterRepository


# class TestTableauRepository:
#
#     @staticmethod
#     def test_publish_workbook():
#         """
#         指定のタブローワークブックがアップロードされていることを確認する
#         :return:
#         """
#         tableau_repository = TableauTwitterRepository()
#         ret = tableau_repository.publish_workbook(
#             project_id=settings.TABLEAU_PUBLISH_PROJECT_ID,
#             workbook_path=settings.APP_ROOT_PATH / "context/tableau/assets/z_twitter.twbx"
#         )
#
#         assert ret.content_url


if __name__ == "__main__":
    pytest.main(["-s"])
