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
  
def limpiar_base_datos():
    try:
        # Establecer conexión a la base de datos
        connection = connect_to_database()  # Debes definir esta función según tu implementación
        
        # Crear el cursor
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM Cliente")
        cursor.execute("DELETE FROM Banco")
        # Eliminar todos los datos de la tabla Factura
        cursor.execute("DELETE FROM Factura")
        
        # Eliminar todos los datos de la tabla Pago
        cursor.execute("DELETE FROM Pago")
        
        # Reiniciar el contador de autoincremento de la tabla Factura (si es necesario)
        cursor.execute("ALTER TABLE Factura AUTO_INCREMENT = 1")
        
        # Reiniciar el contador de autoincremento de la tabla Pago (si es necesario)
        cursor.execute("ALTER TABLE Pago AUTO_INCREMENT = 1")
        
        # Confirmar los cambios en la base de datos
        connection.commit()
        
        print("Base de datos limpiada correctamente.")
    except mysql.connector.Error as error:
        print("Error al limpiar la base de datos:", error)
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()
  
  
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

def insertar_factura(numero_factura, nit_cliente, fecha, valor):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    try:
        try:
            valor = float(valor)
            if valor <=0:
                print(f"Error: El valor de la factura debe ser mayor que cero. Valor ingresado: {valor}")
                control.facturas_error += 1
        except ValueError:
            print(f"Error: El valor de la factura {numero_factura} no es un número decimal válido.")
            control.facturas_error += 1
            return
        
        cursor.execute("SELECT * FROM Factura WHERE NumeroFactura = %s", (numero_factura,))
        existing_factura = cursor.fetchone()
        
        if existing_factura:
            print(f"Factura con número {numero_factura} ya existe en la base de datos.")
            control.facturas_duplicadas += 1
            return
        else:
            cursor.execute("INSERT INTO Factura (NumeroFactura, NITCliente, Fecha, Valor) VALUES (%s, %s, %s, %s)",
                           (numero_factura, nit_cliente, fecha, valor))
            connection.commit()
            print(f"Factura con número {numero_factura} insertada en la base de datos.")
            control.facturas_insertadas += 1
    except mysql.connector.Error as error:
        print("Error al insertar factura:", error)
        control.facturas_error += 1
    finally:
        cursor.close()
        connection.close()

def insertar_pago(codigo_banco, nit_cliente, fecha, valor):
    try:
        # Validar que el valor del pago sea mayor que cero
        if valor <= 0:
            raise ValueError("El valor del pago debe ser mayor que cero.")
        
        connection = connect_to_database()
        cursor = connection.cursor()
        
        # Consulta SQL para insertar el nuevo pago
        insert_query = """
            INSERT INTO Pago (CodigoBanco, NITCliente, Fecha, Valor)
            VALUES (%s, %s, %s, %s)
        """
        # Datos del nuevo pago
        pago_data = (codigo_banco, nit_cliente, fecha, valor)
        
        print(f"Insertando pago de Q{valor} para el cliente con NIT {nit_cliente} en el banco con código {codigo_banco}...")
        # Ejecutar la consulta SQL para insertar el nuevo pago
        cursor.execute(insert_query, pago_data)
        connection.commit()
        
        # Incrementar el contador de pagos insertados
        control.pagos_insertados += 1
        print("Pago insertado correctamente.")
    except ValueError as ve:
        print("Error al insertar pago:", ve)
        control.pagos_error += 1
    except mysql.connector.Error as error:
        # Si ocurre un error durante la inserción, incrementar el contador de pagos con error
        print("Error al insertar pago:", error)
        control.pagos_error += 1
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()

def obtener_info_cliente(nit_cliente):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Cliente WHERE NIT = %s", (nit_cliente,))
        cliente = cursor.fetchone()
        
        if cliente:
            cursor.execute("SELECT * FROM Factura WHERE NITCliente = %s", (nit_cliente,))
            facturas = cursor.fetchall()
            
            cursor.execute("SELECT * FROM Pago WHERE NITCliente = %s", (nit_cliente,))
            pagos = cursor.fetchall()
            
            return cliente, facturas, pagos
        else:
            print(f"No se encontró un cliente con NIT {nit_cliente}")
            return None, None, None
    except mysql.connector.Error as e:
        print("Error al obtener información del cliente:", e)
    

def obtener_info_todos_clientes():
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Consultar todos los clientes
        cursor.execute("SELECT * FROM Cliente")
        clientes = cursor.fetchall()
        
        info_clientes = []
        for cliente in clientes:
            nit_cliente = cliente['NIT']
            
            # Consultar facturas del cliente
            cursor.execute("SELECT * FROM Factura WHERE NITCliente = %s", (nit_cliente,))
            facturas = cursor.fetchall()
            
            # Consultar pagos del cliente
            cursor.execute("SELECT * FROM Pago WHERE NITCliente = %s", (nit_cliente,))
            pagos = cursor.fetchall()
            
            info_clientes.append({
                'cliente': cliente,
                'facturas': facturas,
                'pagos': pagos
            })
        
        return info_clientes
    except mysql.connector.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def obtener_todos_pagos():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Consultar todos los pagos con el nombre del banco
        query = """
            SELECT Pago.CodigoBanco, Banco.Nombre AS NombreBanco, DATE_FORMAT(Pago.Fecha, '%d/%m/%Y') AS FechaFormateada, Pago.Valor
            FROM Pago
            INNER JOIN Banco ON Pago.CodigoBanco = Banco.Codigo

        """
        cursor.execute(query)
        pagos = cursor.fetchall()
        
        return pagos
    except mysql.connector.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
