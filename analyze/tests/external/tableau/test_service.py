from unittest import mock

from tableauserverclient.server import ProjectItem, WorkbookItem

from external.tableau.service import TableauTwitterService


class TestTableauService:
    @staticmethod
    def test_prepare_workbook_area():
        """ タブローオンライン上に専用のワークブックエリア生成後のURL生成が正しく行われているか確認する

        :return:
        """
        from external.tableau.repository import TableauTwitterRepository
        project_item = ProjectItem("test_projects")
        project_item._id = "1"
        workbook_item = WorkbookItem('test_project_id')
        workbook_item._views = [
            type("mockItem", (object,), {
                "content_url": "test_content_url",
            })
        ]

        with mock.patch.object(TableauTwitterRepository, 'create_project', return_value=project_item):
            with mock.patch.object(TableauTwitterRepository, 'publish_workbook', return_value=workbook_item):
                generate_url = TableauTwitterService().prepare_workbook_area('test_user@aaa.com')

                assert generate_url == "https://10az.online.tableau.com/#/site/???/views/test_content_url/README"
