
from injector import inject
from configs.config_wraper import ConfigWrapper
from daos.comparation_group_dao import ComparationGroupDao
from daos.material_dao import MaterialDao
from daos.swap_test_dao import SwapTestDao
import os
import random
from process_code import COMPARATION_GROUP_ALREADY_EXISTS, COMPARATION_GROUP_NOT_EXIST, INVALID_SWAP_TEST, MISMATCH_DATASET, OK
from utils.db_file_util import DbFileUtil


class ComparationGroupService:
    @inject
    def __init__(self, comparation_group_dao: ComparationGroupDao,
                 swap_test_dao: SwapTestDao,
                 material_dao: MaterialDao,
                 db_file_util: DbFileUtil):
        self.comparation_group_dao = comparation_group_dao
        self.swap_test_dao = swap_test_dao
        self.material_dao = material_dao
        self.db_file_util = db_file_util

    def add_comparation_group(self, src_id: int, target_id: int, remark=None):
        src_swap = self.swap_test_dao.query_swap_test(src_id)
        if src_swap is None or len(src_swap) == 0:
            return INVALID_SWAP_TEST
        target_warp = self.swap_test_dao.query_swap_test(target_id)
        if target_warp is None or len(target_warp) == 0:
            return INVALID_SWAP_TEST
        src_swap_id, src_name, src_result_dir, src_dataset_id = src_swap
        target_swap_id, target_name, target_result_dir, target_dataset_id = target_warp
        if src_dataset_id != target_dataset_id:
            return MISMATCH_DATASET
        existed = self.comparation_group_dao.exist_comparation_group(
            src_id, target_id)
        if existed:
            return COMPARATION_GROUP_ALREADY_EXISTS
        self.comparation_group_dao.add_comparation_group(
            src_id, target_id, src_dataset_id, remark)
        return OK

    def list_comparation_group(self, dataset_id=None):
        if dataset_id is None:
            groups = self.comparation_group_dao.list_all_comparation_group()
        else:
            groups = self.comparation_group_dao.list_comparation_group_by_dataset_id(
                dataset_id)
        if len(groups) == 0:
            return []
        swap_id_set = set()
        for group in groups:
            swap_id_set.add(group[1])  # add src_id
            swap_id_set.add(group[2])  # add target_id
        id_names = self.swap_test_dao.query_swap_test_names_by_ids(swap_id_set)
        id_name_dict = dict()
        for _swap_id, name in id_names:
            id_name_dict[_swap_id] = name
        new_groups = []
        for group in groups:
            new_group = []
            src_id, target_id = group[1], group[2]
            for item in group:
                new_group.append(item)
            if src_id in id_name_dict and target_id in id_name_dict:
                new_group.append(id_name_dict[src_id])
                new_group.append(id_name_dict[target_id])
                new_groups.append(new_group)
        return new_groups

    def rank(self, cg_id, random_order=True):
        group = self.comparation_group_dao.query_comparation_group(cg_id)
        if group is None or len(group) == 0:
            return COMPARATION_GROUP_NOT_EXIST, None, None
        src_id, target_id, dataset_id = group[0], group[1], group[2]

        src_swap = self.swap_test_dao.query_swap_test(src_id)
        target_swap = self.swap_test_dao.query_swap_test(target_id)
        materials = self.material_dao.query_materials_by_dataset_id(dataset_id)

        src_name, src_result_dir = src_swap[1], src_swap[2]
        target_name, target_result_dir = target_swap[1], target_swap[2]

        src_swap_result_dir, target_swap_result_dir = \
            self.db_file_util.get_swap_result_dir(
                src_result_dir, target_result_dir)

        pairs = []
        order = []
        for material in materials:
            material_id, basename, mtype = material
            src_path = os.path.join(src_swap_result_dir, basename)
            target_path = os.path.join(target_swap_result_dir, basename)
            src_path = self.db_file_util.get_server_url(src_path)
            target_path = self.db_file_util.get_server_url(target_path)
            if not random_order or random.random() < 0.5:
                pairs.append((mtype, src_path, target_path))
                order.append(1)
            else:
                pairs.append((mtype, target_path, src_path))
                order.append(0)
        return OK, pairs, order

    def query_comparation_group(self, cg_id: int):
        return self.comparation_group_dao.query_comparation_group(cg_id)
