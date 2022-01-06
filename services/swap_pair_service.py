
from genericpath import exists
from injector import inject
from daos.face_dao import FaceDao
from daos.material_dao import MaterialDao
from daos.swap_pair_dao import SwapPairDao
from process_code import BAD_REQUEST, INCONSISTENT_DATA, OK, SWAP_PAIR_ALREADY_IN_DATASET, SWAP_PAIR_EXIST, SWAP_PAIR_NOT_IN_DATASET
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
        code, swap_pairs = self._add_details(db_swap_pairs)
        return code, swap_pairs

    def query_swap_pair_by_spd_id(self, spd_id: int):
        db_swap_pairs = self.swap_pair_dao.query_swap_pair_by_spd_id(spd_id)
        code, swap_pairs = self._add_details(db_swap_pairs)
        return code, swap_pairs

    def query_swap_pair_by_remark(self, remark: str):
        db_swap_pairs = self.swap_pair_dao.query_swap_pair_by_remark(remark)
        code, swap_pairs = self._add_details(db_swap_pairs)
        return code, swap_pairs

    def add_swap_pair(self, face_id: int, material_id: int, remark: str):
        exists = self.swap_pair_dao.exist_swap_pair(face_id, material_id)
        if exists:
            return SWAP_PAIR_EXIST, -1
        sp_id = self.swap_pair_dao.add_swap_pair(face_id, material_id, remark)
        return OK, sp_id

    def add_swap_pair_dataset(self, name: str):
        spd_id = self.swap_pair_dao.add_swap_pair_dataset(name)
        return OK, spd_id

    def add_swap_pair_to_dataset(self, spd_id: int, sp_id: int):
        exists = self.swap_pair_dao.exist_swap_pair_in_dataset(spd_id, sp_id)
        if exists:
            return SWAP_PAIR_ALREADY_IN_DATASET
        self.swap_pair_dao.add_swap_pair_to_dataset(spd_id, sp_id)
        return OK

    def remove_swap_pair_from_dataset(self, spd_id: int, sp_id: int):
        exists = self.swap_pair_dao.exist_swap_pair_in_dataset(spd_id, sp_id)
        if not exists:
            return SWAP_PAIR_NOT_IN_DATASET
        self.swap_pair_dao.remove_swap_pair_from_dataset(spd_id, sp_id)
        return OK

    def query_swap_pair_dataset_list(self, name: str):
        db_swap_pair_dataset_list = self.swap_pair_dao.query_swap_pair_dataset_by_name(
            name)
        swap_pair_dataset_list = self._convert_db_swap_pair_dataset_list(
            db_swap_pair_dataset_list)
        return OK, swap_pair_dataset_list

    def _convert_db_swap_pair_dataset_list(self, db_swap_pair_dataset_list):
        swap_pair_dataset_list = []
        for db_dataset in db_swap_pair_dataset_list:
            dataset = {
                "spd_id": db_dataset[0],
                "name": db_dataset[1]
            }
            swap_pair_dataset_list.append(dataset)
        return swap_pair_dataset_list

    def _add_details(self, db_swap_pairs):
        face_ids = []
        material_ids = []
        swap_pairs = []
        for _, face_id, material_id, _ in db_swap_pairs:
            face_ids.append(face_id)
            material_ids.append(material_id)
        db_faces = self.face_dao.query_faces_by_faceids(face_ids)
        db_materials = self.material_dao.query_materials_by_ids(material_ids)

        faces = self.db_file_util.convert_db_faces(db_faces)
        materials = self.db_file_util.convert_db_materials(db_materials)

        materials_dict = dict()
        faces_dict = dict()
        for face in faces:
            faces_dict[face['face_id']] = face
        for material in materials:
            materials_dict[material['material_id']] = material

        for db_swap_pair in db_swap_pairs:
            face_id = db_swap_pair[1]
            material_id = db_swap_pair[2]
            if face_id not in faces_dict or material_id not in materials_dict:
                return INCONSISTENT_DATA, swap_pairs
            face = faces_dict[face_id]
            material = materials_dict[material_id]
            swap_pair = {
                "sp_id": db_swap_pair[0],
                "face": face,
                "material": material,
                "remark": db_swap_pair[3]
            }
            swap_pairs.append(swap_pair)
        return OK, swap_pairs
