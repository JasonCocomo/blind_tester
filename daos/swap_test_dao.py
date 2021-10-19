from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


query_swap_test_by_id_sql = (
    "SELECT swap_id, name, result_dir, dataset_id FROM swap_test "
    "WHERE swap_id = %(swap_id)s"
)

query_swap_test_name_by_ids_sql = (
    "SELECT swap_id, name FROM swap_test "
    "WHERE swap_id in (%s)"
)


save_swap_test_sql = (
    "INSERT INTO swap_test "
    "(name, result_dir, dataset_id, remark) "
    "VALUES (%(name)s, %(result_dir)s, %(dataset_id)s, %(remark)s)"
)


class SwapTestDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def query_swap_test(self, swap_id):
        cnx = self.cnx_pool.get_connection()
        swap_test = None
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'swap_id': swap_id
                }
                cursor.execute(query_swap_test_by_id_sql, params)
                swap_test = cursor.fetchone()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return swap_test

    def query_swap_test_names_by_ids(self, swap_ids):
        cnx = self.cnx_pool.get_connection()
        id_and_names = []
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                format_strings = ','.join(['%s'] * len(swap_ids))
                cursor.execute(query_swap_test_name_by_ids_sql %
                               format_strings,  tuple(swap_ids))
                id_and_names = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return id_and_names

    def add_swap_test(self, name: str, result_dir: str, dataset_id: int, remark=None):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'name': name.lower(),
                    'result_dir': result_dir,
                    'dataset_id': dataset_id,
                    'remark': remark
                }
                cursor.execute(save_swap_test_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
