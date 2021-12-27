from logging import Logger
from flask import Flask, request
from mysql.connector.pooling import MySQLConnectionPool
from api_result import api_result
from configs.config_wraper import ConfigWrapper
from process_code import BAD_REQUEST, NO_SELECTED_FILE, OK, UNSUPPORTED_FILE_TYPE
from services.comparation_group_service import ComparationGroupService
from services.comparation_result_service import ComparationResultService
from services.dataset_service import DatasetService
from services.face_service import FaceService
from services.file_service import FileService
from services.swap_test_service import SwapTestService
from services.swap_pair_service import SwapPairService
from utils.mysql_helper import init_db_connection_pool
from flask_injector import FlaskInjector
from injector import Binder, Module, singleton
from flask_cors import CORS

config_path = 'configs/server.json'
app = Flask(__name__)
option_files = 'configs/mysql.cnf'
option_groups = 'app_server'
cnx_pool = init_db_connection_pool('app', 5, option_files, option_groups)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)


class MyModule(Module):
    def configure(self, binder: Binder):
        binder.bind(MySQLConnectionPool, to=cnx_pool, scope=singleton)
        binder.bind(ConfigWrapper, to=ConfigWrapper(
            config_path), scope=singleton)
        binder.bind(Logger, to=app.logger)


@app.route("/api/dataset/add", methods=['POST'])
def add_dataset(dataset_service: DatasetService):
    rdata = request.get_json()
    name = rdata['name']
    remark = rdata.get('remark')
    code, dataset_id = dataset_service.create_dataset(name, remark)
    if code != OK:
        return api_result(code=code)
    data = {
        'dataset_id': dataset_id
    }
    return api_result(data=data)


@app.route("/api/material/add", methods=['POST'])
def add_material(dataset_service: DatasetService):
    rdata = request.get_json()
    file_id = rdata['file_id']
    mtype = rdata['mtype']
    remark = rdata['remark']
    code, material_id = dataset_service.create_material(file_id, mtype, remark)
    if code != OK:
        return api_result(code=code)
    data = {
        'material_id': material_id
    }
    return api_result(data=data)


@app.route("/api/material_group/join", methods=['POST'])
def add_material_to_dataset(dataset_service: DatasetService):
    rdata = request.get_json()
    dataset_id = rdata['dataset_id']
    material_id = rdata['material_id']
    code = dataset_service.add_material_to_dataset(dataset_id, material_id)
    return api_result(code=code)

@app.route("/api/material_group/query_joined", methods=['POST'])
def query_materials_joined(dataset_service: DatasetService):
    rdata = request.get_json()
    dataset_id = rdata['dataset_id']
    code, materials = dataset_service.query_materials_joined(dataset_id)
    if code != OK:
        return api_result(code=code)
    data = {
        'materials': materials
    }
    return api_result(data=data)


@app.route("/api/dataset/query", methods=['POST'])
def query_dataset(dataset_service: DatasetService):
    rdata = request.get_json()
    query_text = rdata.get('query_text')
    code, datasets = dataset_service.query_datasets(query_text)
    data = {
        'datasets': datasets
    }
    return api_result(code=code, data=data)


@app.route("/api/swap_test/add", methods=['POST'])
def add_swap_test(swap_test_service: SwapTestService):
    rdata = request.get_json()
    name = rdata['name']
    result_dir = rdata['result_dir']
    dataset_id = rdata['dataset_id']
    remark = rdata.get('remark')
    code = swap_test_service.add_swap_test(
        name, result_dir, dataset_id, remark)
    return api_result(code=code)


@app.route("/api/comparation_group/create", methods=['POST'])
def create_comparation_group(comparation_group_service: ComparationGroupService):
    rdata = request.get_json()
    src_id = rdata['src_id']
    target_id = rdata['target_id']
    remark = rdata.get('remark')
    code = comparation_group_service.add_comparation_group(
        src_id, target_id, remark)
    return api_result(code=code)


@app.route("/api/comparation_group/list", methods=['GET'])
# @cross_origin()
def list_comparation_group(comparation_group_service: ComparationGroupService):
    dataset_id = request.args.get('dataset_id', None, type=int)
    groups = comparation_group_service.list_comparation_group(dataset_id)
    return api_result(code=OK, data=groups)


@app.route("/api/comparation_group/rank", methods=['POST'])
def rank_comparation_group(comparation_group_service: ComparationGroupService):
    rdata = request.get_json()
    cg_id = rdata['cg_id']
    code, pairs, order = comparation_group_service.rank(cg_id)
    if code != OK:
        return api_result(code=code)
    data = {
        "pairs": pairs,
        "order": order,
        'cg_id': cg_id
    }
    return api_result(code=OK, data=data)


@app.route("/api/comparation_result/generate", methods=['POST'])
def generate_comparation_result(comparation_result_service: ComparationResultService):
    rdata = request.get_json()
    cg_id = rdata['cg_id']
    c_order = rdata['order']
    target_scores = rdata['target_scores']
    code, cr_id = comparation_result_service.save_comparation_result(
        cg_id, c_order, target_scores)
    data = {
        "cr_id": cr_id
    }
    return api_result(code=code, data=data)


@app.route("/api/comparation_result/details", methods=['POST'])
def query_comparation_result(comparation_result_service: ComparationResultService,
                             comparation_group_service: ComparationGroupService,
                             swap_test_service: SwapTestService):
    rdata = request.get_json()
    cg_id = rdata['cg_id']
    cr_id = rdata.get('cr_id')
    src_id, target_id, dataset_id = comparation_group_service.query_comparation_group(
        cg_id)
    code, src_name, target_name = swap_test_service.query_src_and_target_names_by_ids(
        src_id, target_id)
    if code != OK:
        return api_result(code=code)
    code, final_model_dim_scores, all_material_dim_scores, cr_material_dim_scores \
        = comparation_result_service.query_comparation_result(cg_id, cr_id)
    if code != OK:
        return api_result(code=code)
    code, pairs, order = comparation_group_service.rank(
        cg_id, random_order=False)
    if code != OK:
        return api_result(code=code)
    data = {
        "cg_id": cg_id,
        "cr_id": cr_id,
        "src_name": src_name,
        "target_name": target_name,
        "pairs": pairs,
        "order": order,
        "model_dim_scores": final_model_dim_scores,
        "all_material_dim_scores": all_material_dim_scores,
        "cr_material_dim_scores": cr_material_dim_scores
    }
    return api_result(code=code, data=data)


def allowed_file(filename, file_type):
    file_types = {
        'face': ['png', 'jpg', 'jpeg'],
        'material': ['gif', 'png', 'jpg', 'jpeg', 'mp4']
    }
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in file_types[file_type]


def not_between(value, min, max):
    return value < min or value > max


@app.route("/api/upload/<file_type>", methods=['POST'])
def upload_file(file_type: str,
                file_service: FileService
                ):
    if file_type not in ['face', 'material']:
        return api_result(code=UNSUPPORTED_FILE_TYPE)
    filekey = 'file'
    if filekey not in request.files:
        return api_result(code=BAD_REQUEST)

    file = request.files.get(filekey)
    if file is None or file.filename == '':
        return api_result(code=NO_SELECTED_FILE)

    if not allowed_file(file.filename, file_type):
        return api_result(code=UNSUPPORTED_FILE_TYPE)

    code, data = file_service.add_file(file, file_type)
    if code != OK:
        return api_result(code=code)
    return api_result(data=data)


@app.route("/api/face/add", methods=['POST'])
def add_face(face_service: FaceService):
    rdata = request.get_json()
    file_id = int(rdata['file_id'])
    skin_color = int(rdata['skin_color'])
    age_range = int(rdata['age_range'])
    gender = int(rdata['gender'])
    roughness = int(rdata['roughness'])
    remark = rdata['remark']
    if not_between(skin_color, 0, 2) \
            or not_between(age_range, 0, 3) \
            or not_between(gender, 0, 1) \
            or not_between(roughness, 0, 4) \
            or remark is None:
        return api_result(code=BAD_REQUEST)

    code, face_id = face_service.add_face(
        file_id, skin_color, age_range, gender, roughness, remark)
    if code != OK:
        return api_result(code=code)
    data = {
        "face_id": face_id
    }
    return api_result(data=data)


@app.route("/api/face/query", methods=['POST'])
def query_face(face_service: FaceService):
    rdata = request.get_json()
    query_text = rdata['query_text']
    if query_text is None:
        return api_result(code=BAD_REQUEST)

    code, faces = face_service.query_faces(query_text)
    if code != OK:
        return api_result(code=code)
    data = {
        "faces": faces
    }
    return api_result(data=data)


@app.route("/api/face/query_joined", methods=['POST'])
def query_joined_face(face_service: FaceService):
    rdata = request.get_json()
    fg_id = rdata['fg_id']
    if fg_id is None or fg_id < 0:
        return api_result(code=BAD_REQUEST)

    code, faces = face_service.query_faces_by_facegroup(fg_id)
    if code != OK:
        return api_result(code=code)
    data = {
        "faces": faces
    }
    return api_result(data=data)


@app.route("/api/face_group/list", methods=['POST'])
def list_face_group(face_service: FaceService):
    code, face_groups = face_service.list_face_groups()
    if code != OK:
        return api_result(code=code)
    data = {
        "face_groups": face_groups
    }
    return api_result(data=data)


@app.route("/api/face_group/create", methods=['POST'])
def add_face_group(face_service: FaceService):
    rdata = request.get_json()
    print(rdata)
    try:
        name = rdata['name']
        remark = rdata['remark']
        if name is None or remark is None or name == "":
            return api_result(code=BAD_REQUEST)
    except Exception:
        return api_result(code=BAD_REQUEST)

    code, fg_id = face_service.add_face_group(name, remark)
    if code != OK:
        return api_result(code=code)
    data = {
        "fg_id": fg_id
    }
    return api_result(data=data)


@app.route("/api/face_group/join", methods=['POST'])
def join_into_face_group(face_service: FaceService):
    rdata = request.get_json()
    fg_id = int(rdata['fg_id'])
    face_id = int(rdata['face_id'])
    if fg_id <= 0 \
            or face_id <= 0:
        return api_result(code=BAD_REQUEST)

    code = face_service.join_into_face_group(fg_id, face_id)
    if code != OK:
        return api_result(code=code)
    return api_result()


@app.route("/api/face_group/remove", methods=['POST'])
def remove_from_face_group(face_service: FaceService):
    rdata = request.get_json()
    fg_id = int(rdata['fg_id'])
    face_id = int(rdata['face_id'])
    if fg_id <= 0 \
            or face_id <= 0:
        return api_result(code=BAD_REQUEST)

    code = face_service.remove_from_face_group(fg_id, face_id)
    if code != OK:
        return api_result(code=code)
    return api_result()


@app.route("/api/swap_pair/add", methods=['POST'])
def add_swap_pair(swap_pair_service: SwapPairService):
    rdata = request.get_json()
    fg_id = int(rdata['face_id'])
    face_id = int(rdata['material_id'])
    remark = rdata['remark']
    if fg_id <= 0 \
            or face_id <= 0 \
            or len(remark) == 0:
        return api_result(code=BAD_REQUEST)

    code, sp_id = swap_pair_service.add_swap_pair(fg_id, face_id, remark)
    if code != OK:
        return api_result(code=code)

    data = {
        'sp_id': sp_id
    }
    return api_result(data=data)


@app.route("/api/swap_pair/query", methods=['POST'])
def query_swap_pairs(swap_pair_service: SwapPairService):
    rdata = request.get_json()
    sp_id = rdata.get('sp_id')
    spd_id = rdata.get('spd_id')
    remark = rdata.get('remark')
    if sp_id is None and spd_id is None and (remark is None or len(remark) == 0):
        return api_result(code=BAD_REQUEST)
    if sp_id is not None:
        sp_id = int(sp_id)
        code, swap_pairs = swap_pair_service.query_swap_pair(sp_id)
    if spd_id is not None:
        spd_id = int(spd_id)
        code, swap_pairs = swap_pair_service.query_swap_pair_by_spd_id(spd_id)
    else:
        code, swap_pairs = swap_pair_service.query_swap_pair_by_remark(remark)

    if code != OK:
        return api_result(code=code)

    data = {
        'swap_pairs': swap_pairs
    }
    return api_result(data=data)


@app.route("/api/swap_pair_dataset/create", methods=['POST'])
def create_swap_pair_dataset(swap_pair_service: SwapPairService):
    rdata = request.get_json()
    name = rdata['name']

    if len(name) == 0:
        return api_result(code=BAD_REQUEST)
    code, spd_id = swap_pair_service.add_swap_pair_dataset(name)

    if code != OK:
        return api_result(code=code)

    data = {
        'spd_id': spd_id
    }
    return api_result(data=data)


@app.route("/api/swap_pair_dataset/join", methods=['POST'])
def join_swap_pair_dataset(swap_pair_service: SwapPairService):
    rdata = request.get_json()
    spd_id = rdata['spd_id']
    sp_id = rdata['sp_id']

    if spd_id <= 0 or sp_id <= 0:
        return api_result(code=BAD_REQUEST)
    code = swap_pair_service.add_swap_pair_to_dataset(spd_id, sp_id)

    if code != OK:
        return api_result(code=code)
    return api_result()


FlaskInjector(app=app, modules=[MyModule])
