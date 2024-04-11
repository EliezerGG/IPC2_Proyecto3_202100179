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
  
  
  
def insert_cliente(NIT, nombre):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Cliente (NIT, Nombre) VALUES (%s, %s)", (NIT, nombre))
        connection.commit()
    except mysql.connector.Error as error:
        print("Error al insertar cliente:", error)
    finally:
        cursor.close()
        connection.close()

def insert_banco(codigo, nombre):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Banco (Codigo, Nombre) VALUES (%s, %s)", (codigo, nombre))
        connection.commit()
    except mysql.connector.Error as error:
        print("Error al insertar banco:", error)
    finally:
        cursor.close()
        connection.close()