from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


query_swap_pair_by_id_sql = (
    "SELECT sp_id, face_id, material_id, remark FROM swap_pair "
    "WHERE sp_id = %(sp_id)s"
)

query_swap_pair_by_swap_pair_dataset_id_sql = (
    "select sp.sp_id, sp.face_id, sp.material_id, sp.remark FROM swap_pair as sp "
    "LEFT JOIN swap_pair_group as spg "
    "ON sp.sp_id = spg.sp_id WHERE spg.spd_id = %(spd_id)s"
)

query_swap_pair_by_remark_sql = (
    "select sp_id, face_id, material_id, remark FROM swap_pair "
    "where remark LIKE '%{}%';"
)

exist_swap_pair_sql = (
    "SELECT count(*) FROM swap_pair "
    "WHERE face_id = %(face_id)s and material_id = %(material_id)s"
)

save_swap_pair_sql = (
    "INSERT INTO swap_pair "
    "(face_id, material_id, remark) "
    "VALUES (%(face_id)s, %(material_id)s, %(remark)s)"
)

save_swap_pair_dataset_sql = (
    "INSERT INTO swap_pair_dataset "
    "(name) "
    "VALUES (%(name)s)"
)

query_swap_pair_dataset_sql = (
    "SELECT spd_id, name FROM swap_pair_dataset "
    "WHERE spd_id = %(spd_id)s"
)

query_swap_pair_dataset_by_name_sql = (
    "SELECT spd_id, name FROM swap_pair_dataset "
    "WHERE name LIKE '%{}%'"
)

add_swap_pair_to_dataset_sql = (
    "INSERT INTO swap_pair_group "
    "(spd_id, sp_id) "
    "VALUES (%(spd_id)s, %(sp_id)s)"
)

exist_swap_pair_in_dataset_sql = (
    "SELECT count(*) FROM swap_pair_group "
    "WHERE spd_id = %(spd_id)s and sp_id = %(sp_id)s"
)

remove_swap_pair_from_dataset_sql = (
    "DELETE FROM swap_pair_group "
    "WHERE spd_id = %(spd_id)s and sp_id = %(sp_id)s"
)


class SwapPairDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def query_swap_pair(self, sp_id):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'sp_id': sp_id
                }
                cursor.execute(query_swap_pair_by_id_sql, params)
                swap_pair = cursor.fetchone()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return swap_pair

    def query_swap_pair_by_spd_id(self, spd_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'spd_id': spd_id
                }
                cursor.execute(
                    query_swap_pair_by_swap_pair_dataset_id_sql, params)
                swap_pairs = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return swap_pairs
    
    def exist_swap_pair_in_dataset(self, spd_id: int,  sp_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'spd_id': spd_id,
                    'sp_id': sp_id
                }
                cursor.execute(
                    exist_swap_pair_in_dataset_sql, params)
                count = cursor.fetchone()
                return count is not None and count[0] > 0
            finally:
                cursor.close()
        finally:
            cnx.close()

    def remove_swap_pair_from_dataset(self, spd_id: int,  sp_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'spd_id': spd_id,
                    'sp_id': sp_id
                }
                cursor.execute(
                    remove_swap_pair_from_dataset_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()

    def query_swap_pair_by_remark(self, remark: str):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                cursor.execute(
                    query_swap_pair_by_remark_sql.format(remark))
                swap_pairs = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return swap_pairs

    def add_swap_pair(self, face_id: int, material_id: int, remark: str):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'face_id': face_id,
                    'material_id': material_id,
                    'remark': remark
                }
                cursor.execute(save_swap_pair_sql, params)
                cnx.commit()
                return cursor.lastrowid
            finally:
                cursor.close()
        finally:
            cnx.close()

    def exist_swap_pair(self, face_id:int, material_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'face_id': face_id,
                    'material_id': material_id
                }
                cursor.execute(exist_swap_pair_sql, params)
                count = cursor.fetchone()
                return count is not None and count[0] > 0
            finally:
                cursor.close()
        finally:
            cnx.close()

    def add_swap_pair_dataset(self, name: str):
        cnx = self.cnx_pool.get_connection()

        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'name': name
                }
                cursor.execute(save_swap_pair_dataset_sql, params)
                cnx.commit()
                return cursor.lastrowid
            finally:
                cursor.close()
        finally:
            cnx.close()

    def query_swap_pair_dataset(self, spd_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'spd_id': spd_id
                }
                cursor.execute(query_swap_pair_dataset_sql, params)
                return cursor.fetchone()
            finally:
                cursor.close()
        finally:
            cnx.close()
    
    def query_swap_pair_dataset_by_name(self, name: str):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                cursor.execute(query_swap_pair_dataset_by_name_sql.format(name))
                return cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()

    def add_swap_pair_to_dataset(self, spd_id: int, sp_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'spd_id': spd_id,
                    'sp_id': sp_id
                }
                cursor.execute(add_swap_pair_to_dataset_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
