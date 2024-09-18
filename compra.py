class Compra:
    _id_incremental = 1

    def __init__(self, cliente, autos):
        self.cliente = cliente
        self.autos = autos
        self.id = Compra._id_incremental
        Compra._id_incremental += 1
        self.costo_total = self.calcular_costo_total()

    def calcular_costo_total(self):
        total = sum(auto.precio_unitario for auto in self.autos)
        return total

    def __str__(self):
        autos_str = "\n".join([str(auto) for auto in self.autos])
        return f"Compra ID: {self.id}\nCliente: {self.cliente}\nAutos:\n{autos_str}\nCosto Total: Q{self.costo_total:.2f}"
