class Cliente:
    def __init__(self, nombre, nit):
        self.nombre = nombre
        self.nit = nit

class Banco:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

class Factura:
    def __init__(self, numero_factura, nit_cliente, fecha, valor):
        self.numero_factura = numero_factura
        self.nit_cliente = nit_cliente
        self.fecha = fecha
        self.valor = valor

class Pago:
    def __init__(self, codigo_banco,fecha, nit_cliente, valor):
        self.codigo_banco = codigo_banco
        self.fecha = fecha
        self.nit_cliente = nit_cliente
        self.valor = valor
    
class Control:
    def __init__(self):
        self.clientes = []
        self.bancos = []
        self.facturas =[]
        self.pagos = []
        self.clientes_actualizados = 0
        self.clientes_insertados = 0
        self.bancos_insertados = 0
        self.bancos_actualizados = 0
        self.facturas_insertadas = 0
        self.facturas_duplicadas = 0
        self.facturas_error = 0
        self.pagos_insertados = 0
        self.pagos_duplicados = 0
        self.pagos_error = 0 
    
    def resetear_datos(self):
        self.clientes_actualizados = 0
        self.clientes_insertados = 0
        self.bancos_insertados = 0
        self.bancos_actualizados = 0
        self.facturas_insertadas = 0
        self.facturas_duplicadas = 0
        self.facturas_error = 0
        self.pagos_insertados = 0
        self.pagos_duplicados = 0
        self.pagos_error = 0
        