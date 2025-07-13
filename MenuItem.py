from abc import ABC, abstractmethod
from collections import deque, namedtuple
import json
import os

# ---------- Clases base del menú ----------

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

class Refresco(ItemMenu):
    def __init__(self, titulo: str, costo: float, medida: str):
        super().__init__(titulo, costo)
        self.medida = medida

    def to_dict(self):
        d = super().to_dict()
        d["medida"] = self.medida
        return d

class Picada(ItemMenu):
    def __init__(self, titulo: str, costo: float, compartir: bool):
        super().__init__(titulo, costo)
        self.compartir = compartir

    def to_dict(self):
        d = super().to_dict()
        d["compartir"] = self.compartir
        return d

class ComidaFuerte(ItemMenu):
    def __init__(self, titulo: str, costo: float, vegetariano: bool):
        super().__init__(titulo, costo)
        self.vegetariano = vegetariano

    def to_dict(self):
        d = super().to_dict()
        d["vegetariano"] = self.vegetariano
        return d

# ---------- namedtuple para combos ----------

Combo = namedtuple("Combo", ["nombre", "items"])

# ---------- Clase Pedido con interfaz para menús ----------

class Pedido:
    def __init__(self):
        self.detalles = []

    def incluir(self, item: ItemMenu):
        self.detalles.append(item)

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

# ---------- FIFO Queue para pedidos ----------

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

# ---------- Ejemplo mínimo ----------

if __name__ == "__main__":
    # Crear algunos ítems
    limonada = Refresco("Limonada Natural", 2.5, "Mediana")
    pasta = ComidaFuerte("Pasta Vegana", 10.5, True)
    nachos = Picada("Nachos con Queso", 6.0, True)

    # Crear combo
    combo_vegano = Combo("Combo Vegano", [limonada, pasta, nachos])

    # Crear menú JSON
    pedido = Pedido()
    pedido.crear_menu("menu_vegano.json", combo_vegano.items)

    # Agregar ítem
    pedido.agregar_al_menu("menu_vegano.json", Refresco("Té Verde", 2.8, "Grande"))

    # Actualizar
    pedido.actualizar_item_menu("menu_vegano.json", "Nachos con Queso", {"costo": 5.5})

    # Eliminar
    pedido.eliminar_del_menu("menu_vegano.json", "Té Verde")

    # Usar la cola
    cola = ColaPedidos()
    cola.agregar_pedido(pedido)
    print(f"Pedidos pendientes: {cola.pedidos_pendientes()}")
