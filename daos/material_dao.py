from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_material_sql = (
    "INSERT INTO material "
    "(mtype, basename, dataset_id) "
    "VALUES (%(mtype)s, %(basename)s, %(dataset_id)s)"
)

query_material_sql = (
    "SELECT material_id, basename, mtype "
    "FROM material "
    "WHERE dataset_id = %(dataset_id)s"
)


class MaterialDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_material(self, mtype: str, basename: str, dataset_id=None, cnx=None):
        commit_and_close = False
        if cnx is None:
            commit_and_close = True
            cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'mtype': mtype.lower(),
                    'basename': basename,
                    'dataset_id': dataset_id
                }
                cursor.execute(save_material_sql, params)
                if commit_and_close:
                    cnx.commit()
            finally:
                cursor.close()
        finally:
            if commit_and_close:
                cnx.close()

    def get_materials(self, dataset_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'dataset_id': dataset_id
                }
                cursor.execute(query_material_sql, params)
                materials = cursor.fetchall()
            finally:
                cursor.close()
            return materials
        finally:
            cnx.close()
