from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_face_sql = (
    "INSERT INTO face "
    "(file_id, filename, skin_color, age_range, gender, roughness, remark) "
    "VALUES (%(file_id)s, %(filename)s, %(skin_color)s, %(age_range)s, %(gender)s, %(roughness)s, %(remark)s)"
)

save_face_group_sql = (
    "INSERT INTO face_group "
    "(name, remark) "
    "VALUES (%(name)s, %(remark)s)"
)

join_into_face_group_sql = (
    "INSERT INTO joined_face_group "
    "(fg_id, face_id) "
    "VALUES (%(fg_id)s, %(face_id)s)"
)

remove_from_face_group_sql = (
    "DELETE FROM joined_face_group "
    "WHERE fg_id = %(fg_id)s and face_id = %(face_id)s"
)

query_face_by_id_sql = (
    "SELECT face_id, file_id, filename "
    "FROM face "
    "WHERE face_id = %(face_id)s"
)

query_face_by_ids_sql = (
    "SELECT face_id, file_id, filename "
    "FROM face "
    "WHERE face_id in ({})"
)

query_faces_by_group_sql = (
    "SELECT face_id "
    "FROM joined_face_group "
    "WHERE fg_id = %(fg_id)s"
)

query_face_by_like_sql = (
    "SELECT face_id, file_id, filename "
    "FROM face "
    "WHERE remark LIKE '%{}%'"
)

query_all_face_groups_sql = (
    "SELECT fg_id, name, remark, status "
    "FROM face_group "
    "ORDER BY fg_id desc"
)

query_face_group_sql = (
    "SELECT name, remark, status "
    "FROM face_group "
    "WHERE fg_id = %(fg_id)s "
    "ORDER BY fg_id desc"
)


update_face_group_status_sql = (
    "UPDATE face_group "
    "SET status = %(status)s "
    "WHERE fg_id = %(fg_id)s"
)


class FaceDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_face(self,
                 file_id: int,
                 filename: str,
                 skin_color: int,
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
                    'skin_color': skin_color,
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

    def query_faces_by_faceids(self, face_ids):
        faces = []
        if len(face_ids) == 0:
            return faces
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                ids_str = ','.join(
                    list(map(lambda face_id: str(face_id), face_ids)))
                cursor.execute(query_face_by_ids_sql.format(ids_str))
                faces = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return faces

    def query_faces_by_group(self, fg_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'fg_id': fg_id
                }
                cursor.execute(query_faces_by_group_sql, params)
                face_ids = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return face_ids

    def query_face_by_face(self, face_id):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    "face_id": face_id
                }
                cursor.execute(query_face_by_id_sql, params)
                face = cursor.fetchone()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return face

    def query_face_by_like(self, query_text):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                cursor.execute(query_face_by_like_sql.format(query_text))
                faces = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return faces

    def query_all_face_groups(self):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                cursor.execute(query_all_face_groups_sql)
                face_group = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return face_group

    def query_face_group(self, fg_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'fg_id': fg_id
                }
                cursor.execute(query_face_group_sql, params)
                face_group = cursor.fetchone()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return face_group

    def join_into_face_group(self, fg_id: int, face_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'fg_id': fg_id,
                    'face_id': face_id
                }
                cursor.execute(join_into_face_group_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()

    def remove_from_face_group(self, fg_id: int, face_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'fg_id': fg_id,
                    'face_id': face_id
                }
                cursor.execute(remove_from_face_group_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()

    def update_face_group_status(self, fg_id: int, new_status: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'fg_id': fg_id,
                    'status': new_status
                }
                cursor.execute(update_face_group_status_sql, params)
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
