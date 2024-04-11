class Cliente:
    def __init__(self, nombre, nit):
        self.nombre = nombre
        self.nit = nit

class Banco:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
        
class Control:
    def __init__(self):
        self.clientes = []
        self.bancos = []
        self.clientes_actualizados = 0
        self.clientes_insertados = 0
        self.bancos_insertados = 0
        self.bancos_actualizados = 0
        