import mysql.connector
from mysql.connector import Error


def db_connect():
    try:
        conn = mysql.connector.connect(host='localhost',database='attendance_webhook',user='root',password='root')
        if conn.is_connected():
            print('Connected to MySQL database.')
            return conn
        else:
            print('DB not Connected.')

    except Error as e:
        print(e.message)
    #
    # finally:
    #     conn.close()


if __name__ == '__main__':
    db_connect()
