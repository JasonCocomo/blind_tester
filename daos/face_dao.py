from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_face_sql = (
    "INSERT INTO face "
    "(file_id, filename, nation, age_range, gender, roughness, remark) "
    "VALUES (%(file_id)s, %(filename)s, %(nation)s, %(age_range)s, %(gender)s, %(roughness)s, %(remark)s)"
)

save_face_group_sql = (
    "INSERT INTO face_group "
    "(name, remark) "
    "VALUES (%(name)s, %(remark)s)"
)

add_to_face_dataset_sql = (
    "INSERT INTO face_dataset "
    "(fg_id, face_id) "
    "VALUES (%(fg_id)s, %(face_id)s)"
)


query_faces_by_group_sql = (
    "SELECT face_id, filename, remark "
    "FROM face "
    "WHERE fg_id = %(fg_id)s"
)


class FaceDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_face(self,
                 file_id: int,
                 filename: str,
                 nation: int,
                 age_range: int,
                 gender: int,
                 roughness: int,
                 remark: str):
        cnx = self.cnx_pool.get_connection()
        lastrow_id = -1
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'file_id': file_id,
                    'filename': filename,
                    'nation': nation,
                    'age_range': age_range,
                    'gender': gender,
                    'roughness': roughness,
                    'remark': remark
                }
                cursor.execute(save_face_sql, params)
                lastrow_id = cursor.lastrowid
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return lastrow_id

    def add_face_group(self, name: str,
                       remark: str):
        cnx = self.cnx_pool.get_connection()
        lastrow_id = -1
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'name': name,
                    'remark': remark
                }
                cursor.execute(save_face_group_sql, params)
                lastrow_id = cursor.lastrowid
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return lastrow_id

    def query_faces_by_group(self, fg_id: int):
        cnx = self.cnx_pool.get_connection()
        faces = []
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'fg_id': fg_id
                }
                cursor.execute(query_faces_by_group_sql, params)
                faces = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return faces

    def add_to_face_dataset(self, face_id, fg_id):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'face_id': face_id,
                    'fg_id': fg_id
                }
                cursor.execute(add_to_face_dataset_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
