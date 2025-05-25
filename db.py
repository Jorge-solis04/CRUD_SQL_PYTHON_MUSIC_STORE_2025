import pymysql
import config

def get_connection():
    return pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        db=config.MYSQL_DB,
        port=config.MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )