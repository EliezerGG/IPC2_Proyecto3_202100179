import mysql.connector
from clases import Control
control = Control()


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
        # Verificar si el cliente ya existe en la base de datos
        cursor.execute("SELECT * FROM Cliente WHERE NIT = %s", (NIT,))
        existing_cliente = cursor.fetchone()

        if existing_cliente:
            # Si el cliente ya existe, actualiza el nombre
            cursor.execute("UPDATE Cliente SET Nombre = %s WHERE NIT = %s", (nombre, NIT))
            print(f"Cliente con NIT {NIT} actualizado con el nombre {nombre}")
            control.clientes_actualizados += 1
        else:
            # Si el cliente no existe, inserta un nuevo registro
            cursor.execute("INSERT INTO Cliente (NIT, Nombre) VALUES (%s, %s)", (NIT, nombre))
            print(f"Nuevo cliente con NIT {NIT} insertado en la base de datos")
            control.clientes_insertados += 1
        
        connection.commit()
    except mysql.connector.Error as error:
        print("Error al insertar o actualizar cliente:", error)
    finally:
        cursor.close()
        connection.close()


def insert_banco(codigo, nombre):
    connection = connect_to_database()
    cursor = connection.cursor()
    try: 
        cursor.execute("SELECT * FROM Banco WHERE Codigo = %s", (codigo,))
        existing_banco = cursor.fetchone()
        
        if existing_banco:
            cursor.execute("UPDATE Banco SET Nombre = %s WHERE Codigo = %s", (nombre, codigo))
            print(f"Banco con código {codigo} actualizado con el nombre {nombre}")
            control.bancos_actualizados += 1
        else:
            cursor.execute("INSERT INTO Banco (Codigo, Nombre) VALUES (%s, %s)", (codigo, nombre))
            print(f"Nuevo banco con código {codigo} insertado en la base de datos")
            control.bancos_insertados += 1
        
        connection.commit()
    except mysql.connector.Error as error:
        print("Error al insertar o actualizar banco:", error)
    finally:
        cursor.close()
        connection.close()