import tableauserverclient as TSC
from tableauserverclient.server import ProjectItem, WorkbookItem


from common import get_logger
import external.tableau as settings


logger = get_logger(__file__)


def get_auth():
    """ TSCの認証情報とサーバ情報の取得

    :return:
    """
    tableau_auth = TSC.TableauAuth(
        settings.TABLEAU_AUTH_USERNAME,
        settings.TABLEAU_AUTH_PASSWORD,
        site_id=settings.TABLEAU_AUTH_SITENAME,
    )
    server = TSC.Server(settings.TABLEAU_AUTH_URL)
    server.version = "3.3"

    return server.auth.sign_in(tableau_auth), server


class TableauTwitterRepository:
    @classmethod
    def create_project(cls, project_name: str, parent_id: str) -> ProjectItem:
        """ タブロープロジェクトの作成
        指定のプロジェクトが存在することを確認し存在すればそのプロジェクト情報を
        存在しなければ、新規に作成する

        :param project_name:
        :param parent_id:
        :return:
        """
        sign_in, server = get_auth()
        with sign_in:
            project_item = cls.has_projects_base_parent_project_id(
                name=project_name, parent_project_id=parent_id
            )
            if project_item is not None:
                return project_item

            new_project = TSC.ProjectItem(name=project_name, parent_id=parent_id)
            return server.projects.create(new_project)

    @classmethod
    def publish_workbook(
        cls, project_id: str, workbook_path: str, file_name: str, connections=None
    ) -> WorkbookItem:
        """ 指定のworkbookをタブローオンラインに公開する

        :param project_id:
        :param workbook_path:
        :param file_name:
        :param connections:
        :return:
        """
        sign_in, server = get_auth()
        with sign_in:
            wb_item = TSC.WorkbookItem(name=file_name, project_id=project_id)
            return server.workbooks.publish(
                wb_item, workbook_path, "CreateNew", connections=connections
            )

    @classmethod
    def publish_datasource(cls, project_id: str, file_path: str):
        """ 指定のデータソースをタブローオンラインに公開する

        :param project_id:
        :param file_path:
        :return:
        """
        new_datasource = TSC.DatasourceItem(project_id)

        sign_in, server = get_auth()
        with sign_in:
            return server.datasources.publish(new_datasource, file_path, "CreateNew")

    @classmethod
    def get_datasource_info(cls, data_source_id: str):
        """ 指定のデータソースの情報を取得する

        :param data_source_id:
        :return:
        """
        sign_in, server = get_auth()
        with sign_in:
            datasource = server.datasources.get_by_id(data_source_id)

            server.datasources.populate_connections(datasource)

            return datasource.connections

    @classmethod
    def get_data_workbook_info(cls, project_id: str):
        """ 指定のワークブック情報を取得する

        :param project_id:
        :return:
        """
        sign_in, server = get_auth()
        with sign_in:
            workbook = server.workbooks.get_by_id(project_id)

            server.workbooks.populate_connections(workbook)

            return workbook.connections

    @classmethod
    def get_all_data_sources(cls):
        """ すべてのデータソース情報を取得する

        :return:
        """
        sign_in, server = get_auth()
        with sign_in:
            return server.datasources.get()

    @classmethod
    def get_all_workbook(cls, req_options):
        """ すべてのworkbook情報を取得する

        :param req_options:
        :return:
        """
        sign_in, server = get_auth()
        with sign_in:
            return server.workbooks.get(req_options=req_options)

    @classmethod
    def get_all_projects(cls, req_option):
        """ すぺてのプロジェクト情報を取得する

        :param req_option:
        :return:
        """
        sign_in, server = get_auth()
        with sign_in:
            return server.projects.get(req_options=req_option)

    @classmethod
    def has_projects_base_parent_project_id(
        cls, name, parent_project_id
    ) -> ProjectItem:
        """ 指定の親以下にプロジェクト情報があるか確認する

        :param name:
        :param parent_project_id:
        :return:
        """
        req_option = TSC.RequestOptions()
        req_option.filter.add(
            TSC.Filter(
                "parentProjectId", TSC.RequestOptions.Operator.Equals, parent_project_id
            )
        )
        req_option.filter.add(
            TSC.Filter("name", TSC.RequestOptions.Operator.Equals, name)
        )

        all_projects_items, pagination_item = cls.get_all_projects(req_option)

        result = all_projects_items[0] if len(all_projects_items) else None

        logger.info('has_projects_base_parent_project_id: name:{} parent_project_id:{} result: {}'.format(name, parent_project_id, result))

        return result


if __name__ == "__main__":
    pass
    # import settings
    # TableauTwitterRepository.has_projects_base_parent_project_id("test", settings.TABLEAU_PUBLISH_BASE_PROJECT_ID)

    # all_workbooks_items, pagination_item = TableauTwitterRepository().get_all_workbook()
    # print([workbook.id for workbook in all_workbooks_items])
    # 855c3a1a-38d5-4328-93c3-95817aee28b9

    # from context.tableau. import TableauTwitterRepository
    # ret = TableauTwitterRepository().publish_workbook(
    #     project_id=settings.TABLEAU_PUBLISH_PROJECT_ID,
    #     workbook_path=settings.APP_ROOT_PATH / "context/tableau/assets/z_twitter.twbx",
    # )

    # ret = TableauTwitterRepository().publish_datasource(
    #     project_id=settings.TABLEAU_PUBLISH_PROJECT_ID,
    #     file_path=settings.APP_ROOT_PATH / "context/tableau/1574757121.0183208-z_twitter.hyper",
    # )

    # datasource_id = "893de2d6-1e1f-4ceb-8fed-aec8db2f4c20"

    # all_projects_items, pagination_item = TableauTwitterRepository.get_all_projects(
    #     req_options="parentProjectId:eq:Viewer:{}".format(settings.TABLEAU_PUBLISH_BASE_PROJECT_ID)
    # )
    # print([(item.id, item.name) for item in all_projects_items])
