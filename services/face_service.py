
from logging import Logger

import configs.keys as keys
from injector import inject
import os
from configs.config_wraper import ConfigWrapper

from daos.face_dao import FaceDao
from daos.file_dao import FileDao
from process_code import INVALID_FACE, OK


class FaceService:
    @inject
    def __init__(self, face_dao: FaceDao,
                 file_dao: FileDao,
                 config_warpper: ConfigWrapper,
                 logger: Logger) -> None:
        self.face_dao = face_dao
        self.file_dao = file_dao
        self.config_warpper = config_warpper
        self.logger = logger

    def add_face(self, file_id: int,
                 nation: int,
                 age_range: int,
                 gender: int,
                 roughness: int,
                 remark: str):
        filename = self.file_dao.query_file(file_id)
        resource_root_dir = self.config_warpper.get(keys.RESOURCE_ROOT_DIR)
        face_root_dir = self.config_warpper.get(keys.FACE_ROOT_DIR)
        face_filepath = os.path.join(
            resource_root_dir, face_root_dir, filename)
        if not os.path.exists(face_filepath) \
                or not os.path.isfile(face_filepath):
            return INVALID_FACE, -1
        face_id = self.face_dao.add_face(
            file_id, filename, nation, age_range, gender, roughness, remark)
        return OK, face_id
