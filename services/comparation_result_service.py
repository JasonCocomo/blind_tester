
from collections import defaultdict
from injector import inject
from daos.comparation_result_dao import ComparationResultDao
from process_code import COMPARATION_RESULT_DATA_COUNT_NOT_RIGHT, COMPARATION_RESULT_NOT_EXIST, INVALID_SCORE, OK


class ComparationResultService:
    @inject
    def __init__(self, comparation_result_dao: ComparationResultDao):
        self.comparation_result_dao = comparation_result_dao
        self.value_separator = ','

    def save_comparation_result(self, cg_id: int, c_order: list, target_scores: dict):
        dim_scores = dict()
        for dim, score in target_scores.items():
            result_score = []
            for c, s in zip(c_order, score):
                if c < 0 or c > 1 or s < 0 or s > 1:
                    return INVALID_SCORE, -1
                result_s = c ^ s ^ 1
                result_score.append(result_s)
            dim_scores[dim] = self.value_separator.join(map(str, result_score))
        order_value = self.value_separator.join(map(str, c_order))
        cr_id = self.comparation_result_dao.add_comparation_result(
            cg_id, order_value, dim_scores)
        return OK, cr_id

    def query_comparation_result(self, cg_id: int, cr_id: int = None):
        cg_result, cg_dim_scores = self.comparation_result_dao.query_comparation_result(
            cg_id)
        cr_orders_dict = dict()
        if len(cg_result) == 0:
            return OK, dict(), list(), list()
        pre_order = None
        for id, c_order in cg_result:
            cr_orders_dict[id] = c_order
            if pre_order is not None and len(pre_order) != len(c_order):
                return COMPARATION_RESULT_DATA_COUNT_NOT_RIGHT, None, None, None
            pre_order = c_order
        material_count = len(pre_order.split(self.value_separator))

        if cr_id is not None:
            if cr_id not in cr_orders_dict.keys():
                return COMPARATION_RESULT_NOT_EXIST, None, None, None

        model_dim_scores = defaultdict(list)
        cr_material_dim_scores = []
        all_material_dim_scores = []
        for i in range(material_count):
            cr_material_dim_scores.append(dict())
            all_material_dim_scores.append(defaultdict(int))

        for id, target_score, score_dim in cg_dim_scores:
            str_scores = target_score.split(self.value_separator)
            material_scores = list(map(int, str_scores))

            for i, mscore in enumerate(material_scores):
                if id == cr_id:
                    cr_material_dim_scores[i][score_dim] = mscore
                all_material_dim_scores[i][score_dim] += mscore
            score = float(sum(material_scores)/material_count)
            model_dim_scores[score_dim].append(score)

        for material_dim_scores in all_material_dim_scores:
            for key in material_dim_scores.keys():
                material_dim_scores[key] = material_dim_scores[key] \
                    / len(cg_dim_scores)
        final_model_dim_scores = dict()
        for dim, scores in model_dim_scores.items():
            final_model_dim_scores[dim] = sum(scores)/len(scores)
        return OK, final_model_dim_scores, all_material_dim_scores, cr_material_dim_scores
