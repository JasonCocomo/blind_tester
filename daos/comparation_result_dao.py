from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_comparation_result_sql = (
    "INSERT INTO comparation_result "
    "(cg_id, `c_order`) "
    "VALUES (%(cg_id)s, %(c_order)s)"
)
save_comparation_result_score_sql = (
    "INSERT INTO comparation_result_score "
    "(cr_id, cg_id, target_score, score_dim) "
    "VALUES (%(cr_id)s, %(cg_id)s, %(target_score)s, %(score_dim)s)"
)

query_comparation_result_by_id_sql = (
    "SELECT cr_id, c_order FROM comparation_result "
    "WHERE cg_id = %(cg_id)s"
)

query_comparation_score_by_result_id_sql = (
    "SELECT cr_id, target_score, score_dim FROM comparation_result_score "
    "WHERE cg_id = %(cg_id)s"
)


class ComparationResultDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_comparation_result(self, cg_id: int, c_order: str, dim_scores: dict):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'cg_id': cg_id,
                    'c_order': c_order
                }
                cursor.execute(save_comparation_result_sql, params)
                cr_id = cursor.lastrowid
                for score_dim, target_score in dim_scores.items():
                    params = {
                        'cr_id': cr_id,
                        'cg_id': cg_id,
                        'target_score': target_score,
                        'score_dim': score_dim
                    }
                    cursor.execute(save_comparation_result_score_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return cr_id

    def query_comparation_result(self, cg_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    "cg_id": cg_id
                }
                cursor.execute(query_comparation_result_by_id_sql, params)
                cg_results = cursor.fetchall()
                cursor.execute(
                    query_comparation_score_by_result_id_sql, params)
                cg_dim_scores = cursor.fetchall()
                return cg_results, cg_dim_scores
            finally:
                cursor.close()
        finally:
            cnx.close()
