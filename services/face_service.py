
from logging import Logger

from injector import inject
from utils.db_file_util import DbFileUtil
from daos.face_dao import FaceDao
from daos.file_dao import FileDao
from process_code import FACE_GROUP_LOCKED, INVALID_FACE_GROUP, OK


class FaceService:
    @inject
    def __init__(self, face_dao: FaceDao,
                 file_dao: FileDao,
                 db_file_util: DbFileUtil,
                 logger: Logger) -> None:
        self.face_dao = face_dao
        self.file_dao = file_dao
        self.db_file_util = db_file_util
        self.logger = logger

    def add_face(self, file_id: int,
                 skin_color: int,
                 age_range: int,
                 gender: int,
                 roughness: int,
                 remark: str):
        filename = self.file_dao.query_file(file_id)
        code = self.db_file_util.check_face(filename)
        if code != OK:
            return code, -1
        face_id = self.face_dao.add_face(
            file_id, filename, skin_color, age_range, gender, roughness, remark)
        return OK, face_id

    def query_faces(self, query_text):
        try:
            face_id = int(query_text)
            face_by_id = self.face_dao.query_face_by_face(face_id)
        except Exception:
            face_by_id = None

        db_faces = self.face_dao.query_face_by_like(query_text)
        if face_by_id is not None:
            db_faces.append(face_by_id)

        faces = self.db_file_util.convert_db_faces(db_faces)
        return OK, faces

    def query_faces_by_facegroup(self, fg_id):
        faceids = self.face_dao.query_faces_by_group(fg_id)
        db_faces = self.face_dao.query_faces_by_faceids(faceids)
        faces = self.db_file_util.convert_db_faces(db_faces)
        return OK, faces

    def list_face_groups(self):
        face_group_tuple_list = self.face_dao.query_all_face_groups()
        face_groups_list = []
        for face_group_tuple in face_group_tuple_list:
            fg_id, name, remark, status = face_group_tuple
            face_group = {
                "fg_id": fg_id,
                "name": name,
                "remark": remark,
                "status": status
            }
            face_groups_list.append(face_group)
        return OK, face_groups_list

    def add_face_group(self, name, remark):
        fg_id = self.face_dao.add_face_group(name, remark)
        return OK, fg_id

    def join_into_face_group(self, fg_id: int, face_id: int):
        face_group = self.face_dao.query_face_group(fg_id)
        if face_group is None or len(face_group) == 0:
            return INVALID_FACE_GROUP
        name, remark, status = face_group
        if status == 1:
            # 表示已经禁止增删人脸，已锁定
            return FACE_GROUP_LOCKED
        self.face_dao.join_into_face_group(fg_id, face_id)
        return OK

    def remove_from_face_group(self, fg_id: int, face_id: int):
        face_group = self.face_dao.query_face_group(fg_id)
        if face_group is None or len(face_group) == 0:
            return INVALID_FACE_GROUP
        name, remark, status = face_group
        if status == 1:
            # 表示已经禁止增删人脸，已锁定
            return FACE_GROUP_LOCKED
        self.face_dao.remove_from_face_group(fg_id, face_id)
        return OK

    def update_face_group_status(self, fg_id, new_status):
        face_group = self.face_dao.query_face_group(fg_id)
        if face_group is None or len(face_group) == 0:
            return INVALID_FACE_GROUP
        self.face_dao.update_face_group_status(fg_id, new_status)
        return OK
