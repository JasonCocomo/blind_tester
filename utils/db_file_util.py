import os

from injector import inject
from configs.config_wraper import ConfigWrapper
import configs.keys as keys
from process_code import INVALID_FACE, OK


class DbFileUtil:
    @inject
    def __init__(self, config_wrapper: ConfigWrapper):
        self.config_wrapper = config_wrapper

    def check_face(self, filename):
        resource_root_dir = self.config_wrapper.get(keys.RESOURCE_ROOT_DIR)
        face_root_dir = self.config_wrapper.get(keys.FACE_ROOT_DIR)
        face_filepath = os.path.join(
            resource_root_dir, face_root_dir, filename)
        if not os.path.exists(face_filepath) \
                or not os.path.isfile(face_filepath):
            return INVALID_FACE
        return OK

    def get_file_path(self, filename, filetype):
        resource_root_dir = self.config_wrapper.get(keys.RESOURCE_ROOT_DIR)
        if filetype == 'face':
            sub_root_dir = self.config_wrapper.get(keys.FACE_ROOT_DIR)
        else:
            sub_root_dir = self.config_wrapper.get(keys.DATASET_ROOT_DIR)

        file_dir = os.path.join(resource_root_dir, sub_root_dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return os.path.join(file_dir, filename)

    def get_server_url(self, file_path):
        resource_root_dir = self.config_wrapper.get(keys.RESOURCE_ROOT_DIR)
        file_server = self.config_wrapper.get(keys.FILE_SERVER)
        return file_path.replace(resource_root_dir, file_server)

    def get_swap_result_dir(self, src_result_dir, target_result_dir):
        resource_root_dir = self.config_warpper.get(keys.RESOURCE_ROOT_DIR)
        swap_result_root_dir = self.config_warpper.get(
            keys.SWAP_RESULT_ROOT_DIR)
        swap_result_dir = os.path.join(resource_root_dir, swap_result_root_dir)
        src_swap_result_dir = os.path.join(swap_result_dir, src_result_dir)
        target_swap_result_dir = os.path.join(
            swap_result_dir, target_result_dir)
        return src_swap_result_dir, target_swap_result_dir

    def convert_db_faces(self, db_faces):
        faces = []
        resource_root_dir = self.config_wrapper.get(keys.RESOURCE_ROOT_DIR)
        face_root_dir = self.config_wrapper.get(keys.FACE_ROOT_DIR)
        file_server = self.config_wrapper.get(keys.FILE_SERVER)
        for db_face in db_faces:
            face_id, file_id, filename = db_face
            face_filepath = os.path.join(
                resource_root_dir, face_root_dir, filename)
            url = face_filepath.replace(resource_root_dir, file_server)
            face = {
                "face_id": face_id,
                "url": url
            }
            faces.append(face)
        return faces

    def convert_db_materials(self, db_materials):
        resource_root_dir = self.config_wrapper.get(keys.RESOURCE_ROOT_DIR)
        dataset_root_dir = self.config_wrapper.get(keys.DATASET_ROOT_DIR)
        file_server = self.config_wrapper.get(keys.FILE_SERVER)

        materials = []
        for db_material in db_materials:
            material_id, basename, mtype = db_material
            material_path = os.path.join(
                resource_root_dir, dataset_root_dir, basename)
            url = material_path.replace(resource_root_dir, file_server)
            material = {
                "material_id": material_id,
                "mtype": mtype,
                "url": url
            }
            materials.append(material)
        return materials
