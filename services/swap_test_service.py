
from injector import inject
from daos.swap_test_dao import SwapTestDao
from process_code import INVALID_SWAP_TEST, OK


class SwapTestService:
    @inject
    def __init__(self, swap_test_dao: SwapTestDao):
        self.swap_test_dao = swap_test_dao

    def add_swap_test(self, name: str, result_dir: str, dataset_id: int, remark):
        self.swap_test_dao.add_swap_test(name, result_dir, dataset_id, remark)
        return OK

    def query_src_and_target_names_by_ids(self, src_id: int, target_id: int):
        id_names = self.swap_test_dao.query_swap_test_names_by_ids(
            [src_id, target_id])
        id_name_dict = dict()
        for id, name in id_names:
            id_name_dict[id] = name
        if src_id not in id_name_dict:
            return INVALID_SWAP_TEST, None, None
        if target_id not in id_name_dict:
            return INVALID_SWAP_TEST, None, None
        return OK, id_name_dict[src_id], id_name_dict[target_id]
