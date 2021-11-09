from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import MySQLConnectionPool
from injector import inject


save_file_sql = (
    "INSERT INTO file "
    "(filename, file_type) "
    "VALUES (%(filename)s, %(file_type)s)"
)

query_file_by_id = (
    "SELECT filename from file "
    "WHERE file_id = %(file_id)s"
)


class FileDao:

    @inject
    def __init__(self, cnx_pool: MySQLConnectionPool):
        self.cnx_pool = cnx_pool

    def add_file(self, filename: str, file_type: str):
        cnx = self.cnx_pool.get_connection()
        lastrow_id = -1
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'filename': filename,
                    'file_type': file_type
                }
                cursor.execute(save_file_sql, params)
                lastrow_id = cursor.lastrowid
                cnx.commit()
            finally:
                cursor.close()
        finally:
            cnx.close()
        return lastrow_id

    def query_file(self, file_id: int):
        cnx = self.cnx_pool.get_connection()
        try:
            cursor: CMySQLCursor = cnx.cursor(cursor_class=CMySQLCursor)
            try:
                params = {
                    'file_id': file_id
                }
                cursor.execute(query_file_by_id, params)
                filename = cursor.fetchone()[0]
            finally:
                cursor.close()
        finally:
            cnx.close()
        return filename
