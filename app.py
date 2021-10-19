from logging import Logger
from flask import Flask, request, render_template
from mysql.connector.pooling import MySQLConnectionPool
from api_result import api_result
from configs.config_wraper import ConfigWrapper
from process_code import OK
from services.comparation_group_service import ComparationGroupService
from services.comparation_result_service import ComparationResultService
from services.dataset_service import DatasetService
from services.swap_test_service import SwapTestService
from utils.mysql_helper import init_db_connection_pool
from flask_injector import FlaskInjector
from injector import Binder, Module, singleton
from flask_cors import CORS

config_path = 'configs/server.json'
app = Flask(__name__)
option_files = 'configs/mysql.cnf'
option_groups = 'app_server'
cnx_pool = init_db_connection_pool('app', 5, option_files, option_groups)
dataset_root_dir_key = 'dataset.root.dir'

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)


class MyModule(Module):
    def configure(self, binder: Binder):
        binder.bind(MySQLConnectionPool, to=cnx_pool, scope=singleton)
        binder.bind(ConfigWrapper, to=ConfigWrapper(
            config_path), scope=singleton)
        binder.bind(Logger, to=app.logger)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/api/dataset/add", methods=['POST'])
def add_dataset(dataset_service: DatasetService):
    rdata = request.get_json()
    name = rdata['name']
    data_dir = rdata['dir']
    remark = rdata.get('remark')
    code = dataset_service.add(name, data_dir, remark)
    return api_result(code=code)


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


FlaskInjector(app=app, modules=[MyModule])
