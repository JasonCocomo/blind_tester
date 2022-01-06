
from logging import Logger

from injector import inject

from daos.dataset_dao import DatasetDao
from daos.file_dao import FileDao
from daos.material_dao import MaterialDao
from utils.db_file_util import DbFileUtil
from process_code import INVALID_MATERIAL, MATERIAL_ALREADY_IN_DATASET, MATERIAL_NOT_IN_DATASET, OK


class DatasetService:
    @inject
    def __init__(self, dataset_dao: DatasetDao,
                 material_dao: MaterialDao,
                 file_dao: FileDao,
                 db_file_util: DbFileUtil,
                 logger: Logger) -> None:
        self.dataset_dao = dataset_dao
        self.material_dao = material_dao
        self.file_dao = file_dao
        self.db_file_util = db_file_util
        self.logger = logger

    def create_dataset(self, name, remark):
        dataset_id = self.dataset_dao.add_dataset(name, remark)
        return OK, dataset_id

    def create_material(self, file_id, mtype, remark):
        basename = self.file_dao.query_file(file_id)
        if basename is None or len(basename) == 0:
            return INVALID_MATERIAL, -1
        material_id = self.material_dao.add_material(
            file_id, basename, mtype, remark)
        return OK, material_id

    def add_material_to_dataset(self, dataset_id, material_id):
        exists = self.material_dao.exists_in_dataset(
            dataset_id, material_id)
        if exists:
            return MATERIAL_ALREADY_IN_DATASET
        self.material_dao.add_to_dataset(dataset_id, material_id)
        return OK

    def remove_material_from_dataset(self, dataset_id, material_id):
        exists = self.material_dao.exists_in_dataset(
            dataset_id, material_id)
        if not exists:
            return MATERIAL_NOT_IN_DATASET
        self.material_dao.remove_from_dataset(dataset_id, material_id)
        return OK

    def query_datasets(self, query_text):
        if query_text is not None:
            datasets = self.dataset_dao.query_datasets(query_text)
        else:
            datasets = self.dataset_dao.list_datasets()
        datasets = self._convert_db_dataset(datasets)
        return OK, datasets

    def _convert_db_dataset(self, db_datasets):
        datasets = []
        for db_dataset in db_datasets:
            dataset = {
                'dataset_id': db_dataset[0],
                'name': db_dataset[1],
                'remark': db_dataset[2]
            }
            datasets.append(dataset)
        return datasets

    def query_materials_by_remark(self, remark: str):
        db_materials = self.material_dao.query_materials_by_remark(remark)
        materials = self.db_file_util.convert_db_materials(db_materials)
        return OK, materials

    def query_materials_joined(self, dataset_id: int):
        db_materials = self.material_dao.query_materials_by_dataset_id(
            dataset_id)
        materials = self.db_file_util.convert_db_materials(db_materials)
        return OK, materials
