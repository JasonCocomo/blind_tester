from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_material_sql = (
    "INSERT INTO material "
    "(file_id, mtype, basename, remark) "
    "VALUES (%(file_id)s, %(mtype)s, %(basename)s, %(remark)s)"
)

add_to_dataset_sql = (
    "INSERT INTO material_group "
    "(dataset_id, material_id) "
    "VALUES (%(dataset_id)s, %(material_id)s)"
)

query_exist_in_dataset_sql = (
    "select count(*) from material_group "
    "where dataset_id = %(dataset_id)s and material_id = %(material_id)s"
)

query_material_by_dataset_id_sql = (
    "SELECT m.material_id, m.basename, m.mtype "
    "FROM material as m LEFT JOIN material_group as mg "
    "on m.material_id = mg.material_id where mg.dataset_id = %(dataset_id)s "
)

query_materials_by_ids_sql = (
    "SELECT material_id, basename, mtype "
    "FROM material "
    "WHERE material_id in ({})"
)


class MaterialDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_material(self, file_id: int, basename: str, mtype: str, remark: str):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'file_id': file_id,
                    'mtype': mtype.lower(),
                    'basename': basename,
                    'remark': remark
                }
                cursor.execute(save_material_sql, params)
                cnx.commit()
                return cursor.lastrowid
            finally:
                cursor.close()
        finally:
            cnx.close()

    def not_exists_in_dataset(self, dataset_id, material_id):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'dataset_id': dataset_id,
                    'material_id': material_id
                }
                cursor.execute(query_exist_in_dataset_sql, params)
                count = cursor.fetchone()
                return count is None
            finally:
                cursor.close()
        finally:
            cnx.close()

    def add_to_dataset(self, dataset_id, material_id):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'dataset_id': dataset_id,
                    'material_id': material_id
                }
                cursor.execute(add_to_dataset_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()

    def query_materials_by_dataset_id(self, dataset_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'dataset_id': dataset_id
                }
                cursor.execute(query_material_by_dataset_id_sql, params)
                materials = cursor.fetchall()
            finally:
                cursor.close()
            return materials
        finally:
            cnx.close()

    def query_materials_by_ids(self, material_ids):
        materials = []
        if len(material_ids) == 0:
            return materials
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                ids_str = ','.join(
                    list(map(lambda material_id: str(material_id), material_ids)))
                cursor.execute(query_materials_by_ids_sql.format(ids_str))
                materials = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return materials
