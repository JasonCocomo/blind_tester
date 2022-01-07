from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_comparation_group_sql = (
    "INSERT INTO comparation_group "
    "(src_id, target_id, spd_id, remark) "
    "VALUES (%(src_id)s, %(target_id)s, %(spd_id)s, %(remark)s)"
)
list_all_comparation_group_sql = (
    "SELECT * from comparation_group "
    "order by cg_id desc"
)
list_comparation_group_by_dataset_sql = (
    "SELECT * from comparation_group "
    "WHERE dataset_id = %(dataset_id)s order by cg_id desc"
)
query_comparation_group_by_src_target_sql = (
    "SELECT * from comparation_group "
    "WHERE src_id = %(src_id)s and target_id = %(target_id)s"
)

query_comparation_group_by_cg_id_sql = (
    "SELECT src_id, target_id, spd_id from comparation_group "
    "WHERE cg_id = %(cg_id)s"
)


class ComparationGroupDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def list_all_comparation_group(self):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                cursor.execute(list_all_comparation_group_sql)
                groups = cursor.fetchall()
            finally:
                cursor.close()
            return groups
        finally:
            cnx.close()

    def list_comparation_group_by_dataset_id(self, dataset_id: int):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'dataset_id': dataset_id
                }
                cursor.execute(
                    list_comparation_group_by_dataset_sql, params)
                groups = cursor.fetchall()
            finally:
                cursor.close()
            return groups
        finally:
            cnx.close()

    def exist_comparation_group(self, src_id: int, target_id: int):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'src_id': src_id,
                    'target_id': target_id
                }
                cursor.execute(
                    query_comparation_group_by_src_target_sql, params)
                comparation_group = cursor.fetchone()
            finally:
                cursor.close()
            return comparation_group is not None and len(comparation_group) > 0
        finally:
            cnx.close()

    def query_comparation_group(self, cg_id: int):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'cg_id': cg_id
                }
                cursor.execute(
                    query_comparation_group_by_cg_id_sql, params)
                comparation_group = cursor.fetchone()
            finally:
                cursor.close()
            return comparation_group
        finally:
            cnx.close()

    def add_comparation_group(self, src_id: int, target_id: int, spd_id: int, remark=None):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'src_id': src_id,
                    'target_id': target_id,
                    'spd_id': spd_id,
                    'remark': remark
                }
                cursor.execute(save_comparation_group_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
