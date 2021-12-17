
from logging import Logger
import uuid
from injector import inject
from daos.file_dao import FileDao
from process_code import OK
from utils.db_file_util import DbFileUtil


class FileService:
    @inject
    def __init__(self, file_dao: FileDao,
                 db_file_util: DbFileUtil,
                 logger: Logger) -> None:
        self.file_dao = file_dao
        self.db_file_util = db_file_util
        self.logger = logger

    def add_file(self, file, file_type: str):
        filename = str(uuid.uuid1()) + '.png'
        file_path = self.db_file_util.get_face_path(filename)
        file.save(file_path)
        file_id = self.file_dao.add_file(filename, file_type)
        url = self.db_file_util.get_server_url(file_path)
        data = {
            'file_id': file_id,
            'url': url
        }
        return OK, data
