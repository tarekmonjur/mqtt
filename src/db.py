import mysql.connector
from mysql.connector import Error


def connect():
    try:
        conn = mysql.connector.connect(host='localhost',database='dbn_attendance',user='root',password='root')
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn

    except Error as e:
        print(e)

    finally:
        conn.close()


def db():
    DB = connect()
    DB.cursor()
    return DB


if __name__ == '__main__':
    connect()