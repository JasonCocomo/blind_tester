
from logging import Logger

from injector import inject
from configs.config_wraper import ConfigWrapper
from daos.file_dao import FileDao
from process_code import OK


class FileService:
    @inject
    def __init__(self, file_dao: FileDao,
                 config_warpper: ConfigWrapper,
                 logger: Logger) -> None:
        self.file_dao = file_dao
        self.config_warpper = config_warpper
        self.logger = logger

    def add_file(self, filename: str, file_type: str):
        face_id = self.file_dao.add_file(filename, file_type)
        return OK, face_id
