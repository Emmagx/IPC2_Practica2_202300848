class Cliente:
    def __init__(self, nombre, correo, nit):
        self.nombre = nombre
        self.correo = correo
        self.nit = nit

    def __str__(self):
        return f"{self.nombre}, {self.correo}, NIT: {self.nit}"
