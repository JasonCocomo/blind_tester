from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_dataset_sql = (
    "INSERT INTO dataset "
    "(name, data_dir, remark) "
    "VALUES (%(name)s, %(data_dir)s, %(remark)s)"
)


class DataSetDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_dataset(self, name, data_dir, remark=None, cnx=None):
        commit_and_close = False
        if cnx is None:
            commit_and_close = True
            cnx = self.cnx_pool.get_connection()
        lastrow_id = -1
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'name': name,
                    'data_dir': data_dir,
                    'remark': remark
                }
                cursor.execute(save_dataset_sql, params)
                lastrow_id = cursor.lastrowid
                if commit_and_close:
                    cnx.commit()
            finally:
                cursor.close()
        finally:
            if commit_and_close:
                cnx.close()
        return lastrow_id
