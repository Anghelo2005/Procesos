class Carrito:
    def __init__(self):
        self.items = []

    def agregar_producto(self, producto):
        self.items.append(producto)

    def calcular_total(self):
        total = sum(item.precio for item in self.items)  
        return total