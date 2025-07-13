from abc import ABC, abstractmethod
from collections import deque, namedtuple
import json
import os

# Elemento base del menú
class ItemMenu(ABC):
    def __init__(self, titulo: str, costo: float):
        self.titulo = titulo
        self.costo = costo

    def obtener_precio(self) -> float:
        return self.costo

    def to_dict(self):
        return {"titulo": self.titulo, "costo": self.costo, "tipo": self.__class__.__name__}

    def __str__(self) -> str:
        return f"{self.titulo} - ${self.costo:.2f}"

# Bebida específica
class Refresco(ItemMenu):
    def __init__(self, titulo: str, costo: float, medida: str):
        super().__init__(titulo, costo)
        self.medida = medida

    def to_dict(self):
        d = super().to_dict()
        d["medida"] = self.medida
        return d

    def __str__(self) -> str:
        return f"{self.titulo} [{self.medida}] - ${self.costo:.2f}"

# Aperitivo
class Picada(ItemMenu):
    def __init__(self, titulo: str, costo: float, compartir: bool):
        super().__init__(titulo, costo)
        self.compartir = compartir

    def to_dict(self):
        d = super().to_dict()
        d["compartir"] = self.compartir
        return d

# Plato principal
class ComidaFuerte(ItemMenu):
    def __init__(self, titulo: str, costo: float, vegetariano: bool):
        super().__init__(titulo, costo)
        self.vegetariano = vegetariano

    def to_dict(self):
        d = super().to_dict()
        d["vegetariano"] = self.vegetariano
        return d

# ✅ namedtuple para combos
Combo = namedtuple("Combo", ["nombre", "items"])

# ✅ Clase iterable para el catálogo
class CatalogoIterable:
    def __init__(self, items=None):
        self._items = items or []

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

# ✅ Clase Pedido con interfaz para manejar menús
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

    # ✅ Interfaz para manejar menús (CRUD)
    def crear_menu(self, nombre_archivo: str, items: list):
        datos = [item.to_dict() for item in items]
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        print(f"✅ Menú guardado en {nombre_archivo}")

    def agregar_al_menu(self, nombre_archivo: str, item: ItemMenu):
        datos = []
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        datos.append(item.to_dict())
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        print(f"➕ Item agregado a {nombre_archivo}")

    def eliminar_del_menu(self, nombre_archivo: str, titulo: str):
        if not os.path.exists(nombre_archivo):
            print("❌ Menú no encontrado.")
            return
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        datos = [i for i in datos if i["titulo"] != titulo]
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        print(f"🗑️ Item '{titulo}' eliminado de {nombre_archivo}")

    def actualizar_item_menu(self, nombre_archivo: str, titulo: str, nuevos_valores: dict):
        if not os.path.exists(nombre_archivo):
            print("❌ Menú no encontrado.")
            return
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        actualizado = False
        for item in datos:
            if item["titulo"] == titulo:
                item.update(nuevos_valores)
                actualizado = True
                break
        if actualizado:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4)
            print(f"✏️ Item '{titulo}' actualizado.")
        else:
            print(f"⚠️ Item '{titulo}' no encontrado.")

# ✅ Cola FIFO para múltiples pedidos
class ColaPedidos:
    def __init__(self):
        self._cola = deque()

    def agregar_pedido(self, pedido: Pedido):
        self._cola.append(pedido)

    def atender_siguiente(self):
        if self._cola:
            return self._cola.popleft()
        else:
            print("📭 No hay pedidos por atender.")
            return None

    def pedidos_pendientes(self):
        return len(self._cola)

# Menú disponible (catálogo inicial)
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

# 🧪 Ejemplo de uso
if __name__ == "__main__":
    catalogo_iterable = CatalogoIterable(catalogo)
    catalogo_iterable.mostrar_todos()

    # Crear un pedido
    pedido1 = Pedido()
    pedido1.incluir(catalogo_iterable[1])
    pedido1.incluir(catalogo_iterable[3])
    pedido1.incluir(catalogo_iterable[5])
    pedido1.incluir(catalogo_iterable[8])
    pedido1.mostrar_resumen()

    # Agregar a cola de pedidos
    cola = ColaPedidos()
    cola.agregar_pedido(pedido1)
    print(f"\n📦 Pedidos en cola: {cola.pedidos_pendientes()}")

    # Guardar menú en JSON
    pedido1.crear_menu("menu_principal.json", catalogo)

    # Actualizar item del menú
    pedido1.actualizar_item_menu("menu_principal.json", "Espresso", {"costo": 3.50})

    # Eliminar item del menú
    pedido1.eliminar_del_menu("menu_principal.json", "Tofu Stir-Fry")

    # Agregar nuevo item
    pedido1.agregar_al_menu("menu_principal.json", Refresco("Jugo de Mango", 3.20, "Grande"))
