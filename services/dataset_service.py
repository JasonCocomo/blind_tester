
from collections import defaultdict
from logging import Logger

from mysql.connector.pooling import MySQLConnectionPool
import configs.keys as keys
from injector import inject
import os
from configs.config_wraper import ConfigWrapper

from daos.dataset_dao import DataSetDao
from daos.material_dao import MaterialDao
from process_code import DB_FAILED_TO_SAVE, INVALID_DATASET, OK


class DatasetService:
    @inject
    def __init__(self, dataset_dao: DataSetDao,
                 material_dao: MaterialDao,
                 cnx_pool: MySQLConnectionPool,
                 config_warpper: ConfigWrapper,
                 logger: Logger) -> None:
        self.dataset_dao = dataset_dao
        self.material_dao = material_dao
        self.cnx_pool = cnx_pool
        self.config_warpper = config_warpper
        self.logger = logger

    def add(self, name, data_dir, remark):
        resource_root_dir = self.config_warpper.get(keys.RESOURCE_ROOT_DIR)
        dataset_root_dir = self.config_warpper.get(keys.DATASET_ROOT_DIR)
        dataset_dir = os.path.join(
            resource_root_dir, dataset_root_dir, data_dir)
        type_dirs = os.listdir(dataset_dir)
        typed_materials = defaultdict(list)
        for type_dir in type_dirs:
            data_dir = os.path.join(dataset_dir, type_dir)
            data_list = os.listdir(data_dir)
            for basename in data_list:
                data_path = os.path.join(data_dir, basename)
                if os.path.isfile(data_path):
                    typed_materials[type_dir].append(basename)
        no_data_found = True
        for key, data_list in typed_materials.items():
            if len(data_list) > 0:
                no_data_found = False
        if no_data_found:
            return INVALID_DATASET

        cnx = self.cnx_pool.get_connection()
        try:

            dataset_id = self.dataset_dao.add_dataset(
                name, data_dir, remark=remark, cnx=cnx)
            if dataset_id < 0:
                self.logger.warning(f'failed to save dataset: {name}')
                return DB_FAILED_TO_SAVE
            for key, data_list in typed_materials.items():
                for basename in data_list:
                    self.material_dao.add_material(
                        key, basename, dataset_id, cnx=cnx)
            cnx.commit()
            return OK
        finally:
            cnx.close()
