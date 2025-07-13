from abc import ABC, abstractmethod

# Elemento base del menú
class ItemMenu(ABC):
    def __init__(self, titulo: str, costo: float):
        self.titulo = titulo
        self.costo = costo

    def obtener_precio(self) -> float:
        return self.costo

    def __str__(self) -> str:
        return f"{self.titulo} - ${self.costo:.2f}"

# Bebida específica
class Refresco(ItemMenu):
    def __init__(self, titulo: str, costo: float, medida: str):
        super().__init__(titulo, costo)
        self.medida = medida

    def __str__(self) -> str:
        return f"{self.titulo} [{self.medida}] - ${self.costo:.2f}"

# Aperitivo
class Picada(ItemMenu):
    def __init__(self, titulo: str, costo: float, compartir: bool):
        super().__init__(titulo, costo)
        self.compartir = compartir

# Plato principal
class ComidaFuerte(ItemMenu):
    def __init__(self, titulo: str, costo: float, vegetariano: bool):
        super().__init__(titulo, costo)
        self.vegetariano = vegetariano

# Manejo del pedido
class Pedido:
    def __init__(self):
        self.detalles = []

    def incluir(self, producto: ItemMenu):
        self.detalles.append(producto)

    def mostrar_resumen(self):
        print("\n🧾 Pedido Final:")
        for prod in self.detalles:
            print(f" • {prod}")
        print(f"\nTotal a pagar: ${self.total_con_descuento():.2f}")

    def total_bruto(self) -> float:
        return sum(p.obtener_precio() for p in self.detalles)

    def total_con_descuento(self) -> float:
        bruto = self.total_bruto()
        return bruto * 0.90 if len(self.detalles) > 3 else bruto

# Nueva clase iterable para el catálogo
class CatalogoIterable:
    def __init__(self, items):
        self._items = items

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def agregar_item(self, item):
        self._items.append(item)

    def mostrar_todos(self):
        print("📋 Catálogo completo:")
        for item in self._items:
            print(f" • {item} ({type(item).__name__})")

# Menú disponible
catalogo = [
    Refresco("Limonada Natural", 2.50, "Mediana"),
    Refresco("Espresso", 3.00, "Chico"),
    Refresco("Té Frutal", 2.75, "Grande"),
    Picada("Spring Rolls", 5.50, True),
    Picada("Tostadas con Ajo", 4.00, False),
    ComidaFuerte("Pechuga Grillada", 12.00, False),
    ComidaFuerte("Pasta Vegana", 10.50, True),
    ComidaFuerte("Burger Clásica", 11.25, False),
    ComidaFuerte("Tofu Stir-Fry", 9.75, True),
    Picada("Nachos con Queso", 6.00, True)
]

# Simulación de pedido
if __name__ == "__main__":
    # Crear el catálogo como iterable
    catalogo_iterable = CatalogoIterable(catalogo)

    # Mostrar el catálogo
    catalogo_iterable.mostrar_todos()

    # Crear y mostrar pedido
    mi_pedido = Pedido()
    mi_pedido.incluir(catalogo_iterable[1])  # Espresso
    mi_pedido.incluir(catalogo_iterable[3])  # Spring Rolls
    mi_pedido.incluir(catalogo_iterable[5])  # Pechuga
    mi_pedido.incluir(catalogo_iterable[8])  # Tofu
    mi_pedido.mostrar_resumen()
