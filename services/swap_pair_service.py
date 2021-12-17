
from injector import inject
from daos.face_dao import FaceDao
from daos.material_dao import MaterialDao
from daos.swap_pair_dao import SwapPairDao
from process_code import BAD_REQUEST, INCONSISTENT_DATA, OK
from utils.db_file_util import DbFileUtil


class SwapPairService:
    @inject
    def __init__(self, swap_pair_dao: SwapPairDao,
                 face_dao: FaceDao,
                 material_dao: MaterialDao,
                 db_file_util: DbFileUtil):
        self.swap_pair_dao = swap_pair_dao
        self.face_dao = face_dao
        self.material_dao = material_dao
        self.db_file_util = db_file_util

    def query_swap_pair(self, sp_id):
        db_swap_pair = self.swap_pair_dao.query_swap_pair(sp_id)
        if len(db_swap_pair) == 0:
            return OK, []
        db_swap_pairs = [db_swap_pair]
        swap_pairs = self._add_details(db_swap_pairs)
        return OK, swap_pairs

    def query_swap_pair_by_spd_id(self, spd_id: int):
        db_swap_pairs = self.swap_pair_dao.query_swap_pair_by_spd_id(spd_id)
        swap_pairs = self._add_details(db_swap_pairs)
        return OK, swap_pairs

    def query_swap_pair_by_remark(self, remark: str):
        db_swap_pairs = self.swap_pair_dao.query_swap_pair_by_remark(remark)
        swap_pairs = self._add_details(db_swap_pairs)
        return OK, swap_pairs

    def add_swap_pair(self, face_id: int, material_id: int, remark: str):
        sp_id = self.swap_pair_dao.add_swap_pair(face_id, material_id, remark)
        return OK, sp_id

    def add_swap_pair_dataset(self, name: str):
        spd_id = self.swap_pair_dao.add_swap_pair_dataset(name)
        return OK, spd_id

    def add_swap_pair_to_dataset(self, spd_id: int, sp_id: int):
        spd = self.swap_pair_dao.query_swap_pair_by_spd_id(spd_id)
        if spd is None or len(spd) == 0:
            return BAD_REQUEST
        self.swap_pair_dao.add_swap_pair_to_dataset(spd_id, sp_id)
        return OK

    def _add_details(self, db_swap_pairs):
        face_ids = []
        material_ids = []
        swap_pairs = []
        for _, face_id, material_id, _ in db_swap_pairs:
            face_ids.append(face_id)
            material_ids.append(material_id)
        db_faces = self.face_dao.query_faces_by_faceids(face_ids)
        db_materials = self.material_dao.query_materials_by_ids(material_ids)
        if len(db_swap_pairs) != len(db_faces) or len(db_faces) != len(db_materials):
            return INCONSISTENT_DATA, swap_pairs
        faces = self.db_file_util.convert_db_faces(db_faces)
        materials = self.db_file_util.convert_db_materials(db_materials)
        for db_swap_pair, face, material in zip(db_swap_pairs, faces, materials):
            swap_pair = {
                "sp_id": db_swap_pair[0],
                "face": face,
                "material": material,
                "remark": db_swap_pair[3]
            }
            swap_pairs.append(swap_pair)
        return OK, swap_pairs
