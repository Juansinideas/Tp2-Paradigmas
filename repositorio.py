import json
import os
from abc import ABC, abstractmethod

from modelos import PedidoDelivery, PedidoRetiro


class RepositorioPedidos(ABC):

    @abstractmethod
    def guardar_todos(self, pedidos):
        raise NotImplementedError

    @abstractmethod
    def cargar_todos(self):
        raise NotImplementedError


class RepositorioJSON(RepositorioPedidos):

    # Mapa clave-guardada -> clase concreta, usado para reconstruir
    # el objeto correcto al leer el JSON (polimorfismo al cargar datos).
    _MAPA_TIPOS = {
        'PedidoDelivery': PedidoDelivery,
        'PedidoRetiro': PedidoRetiro,
    }

    def __init__(self, ruta_archivo='pedidos.json'):
        self._ruta = ruta_archivo

    def guardar_todos(self, pedidos):
        datos = [p.to_dict() for p in pedidos]
        try:
            with open(self._ruta, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except OSError as error:
            print(f'ERROR: No se pudo guardar en disco. {error}')
            return False

    def cargar_todos(self):
        if not os.path.exists(self._ruta):
            return []  # igual que el Pascal: si no existe el archivo, no carga nada

        try:
            with open(self._ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except (OSError, json.JSONDecodeError) as error:
            print(f'ERROR: No se pudo leer el archivo de pedidos. {error}')
            return []

        return [self._reconstruir_pedido(item) for item in datos]

    def _reconstruir_pedido(self, item):
        clase = self._MAPA_TIPOS.get(item.get('tipo'), PedidoRetiro)

        if clase is PedidoDelivery:
            pedido = PedidoDelivery(
                item['id'], item['cliente'], item['detalle'],
                item['total'], item.get('direccion', 'Sin direccion'),
            )
        else:
            pedido = PedidoRetiro(item['id'], item['cliente'], item['detalle'], item['total'])

        # Restauramos estado interno tal como estaba guardado
        pedido._estado = item.get('estado', 'Pendiente')
        pedido._cancelado = item.get('cancelado', False)
        pedido._fecha_creacion = item.get('fecha_creacion', '')
        return pedido
