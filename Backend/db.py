import mysql.connector


def connect_to_database():
    config = {
      'user': 'usuario',
      'password': 'secreto',
      'host': 'localhost',
      'database': 'banca_virtual',
      'raise_on_warnings': True
    }

    connection = mysql.connector.connect(**config)

    return connection