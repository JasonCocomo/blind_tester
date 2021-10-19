import mysql.connector as mc
import mysql.connector.pooling as mcp


def init_db_connection_pool(pool_name,
                            pool_size,
                            option_files,
                            option_groups):
    return mcp.MySQLConnectionPool(pool_name=pool_name,
                                   pool_size=pool_size,
                                   option_files=option_files,
                                   option_groups=option_groups)


def init_db_connection(option_files,
                       option_groups):
    return mc.connect(option_files=option_files,
                      option_groups=option_groups)
