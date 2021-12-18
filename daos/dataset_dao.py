from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_dataset_sql = (
    "INSERT INTO dataset "
    "(name, remark) "
    "VALUES (%(name)s, %(remark)s)"
)

query_dataset_sql = (
    "SELECT id, name, remark FORM dataset "
    "WHERE name like '{}'"
)

list_dataset_sql = (
    "SELECT id, name, remark FORM dataset "
)


class DatasetDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_dataset(self, name, remark):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'name': name,
                    'remark': remark
                }
                cursor.execute(save_dataset_sql, params)
                cnx.commit()
                return cursor.lastrowid
            finally:
                cursor.close()
        finally:
            cnx.close()

    def query_datasets(self, query_text):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                cursor.execute(query_dataset_sql.format(query_text))
                return cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()

    def list_datasets(self):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                cursor.execute(list_dataset_sql)
                return cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
