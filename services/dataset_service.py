
from logging import Logger

from injector import inject

from daos.dataset_dao import DatasetDao
from daos.file_dao import FileDao
from daos.material_dao import MaterialDao
from process_code import INVALID_MATERIAL, MATERIAL_ALREADY_IN_DATASET, OK


class DatasetService:
    @inject
    def __init__(self, dataset_dao: DatasetDao,
                 material_dao: MaterialDao,
                 file_dao: FileDao,
                 logger: Logger) -> None:
        self.dataset_dao = dataset_dao
        self.material_dao = material_dao
        self.file_dao = file_dao
        self.logger = logger

    def create_dataset(self, name, remark):
        dataset_id = self.dataset_dao.add_dataset(name, remark)
        return OK, dataset_id

    def create_material(self, file_id, mtype, remark):
        file_item = self.file_dao.query_file(file_id)
        if file_item is None or len(file_item) == 0:
            return INVALID_MATERIAL, -1
        basename = file_item[0]
        material_id = self.material_dao.add_material(
            file_id, basename, mtype, remark)
        return OK, material_id

    def add_material_to_dataset(self, dataset_id, material_id):
        not_exist = self.material_dao.not_exists_in_dataset(
            dataset_id, material_id)
        if not not_exist:
            return MATERIAL_ALREADY_IN_DATASET
        self.material_dao.add_to_dataset(dataset_id, material_id)
        return OK

    def query_datasets(self, query_text):
        if query_text is not None:
            datasets = self.dataset_dao.query_datasets(query_text)
        else:
            self.dataset_dao.list_datasets()
        return OK, datasets
