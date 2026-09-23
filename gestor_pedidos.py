from modelos import PedidoDelivery, PedidoRetiro
from repositorio import RepositorioJSON


class GestorPedidos:
    def __init__(self, repositorio=None):
        self._repositorio = repositorio if repositorio is not None else RepositorioJSON()
        self._pedidos = self._repositorio.cargar_todos()

    @property
    def pedidos(self):
        return list(self._pedidos)

    def _siguiente_id(self):
        if not self._pedidos:
            return 1
        return max(p.id for p in self._pedidos) + 1

    def _guardar(self):
        return self._repositorio.guardar_todos(self._pedidos)

    # ---------------- Alta de pedidos ----------------
    def crear_pedido_delivery(self, cliente, detalle, total, direccion):
        nuevo = PedidoDelivery(self._siguiente_id(), cliente, detalle, total, direccion)
        self._pedidos.append(nuevo)
        self._guardar()
        return nuevo

    def crear_pedido_retiro(self, cliente, detalle, total):
        nuevo = PedidoRetiro(self._siguiente_id(), cliente, detalle, total)
        self._pedidos.append(nuevo)
        self._guardar()
        return nuevo

    # ---------------- Consultas ----------------
    def buscar_por_id(self, id_pedido):
        for pedido in self._pedidos:
            if pedido.id == id_pedido:
                return pedido
        return None

    def listar_pendientes(self):
        return [p for p in self._pedidos if not p.cancelado and p.estado == 'Pendiente']

    def listar_entregados(self):
        return [p for p in self._pedidos if not p.cancelado and p.estado == 'Entregado']

    # ---------------- Modificacion ----------------
    def modificar_cliente(self, id_pedido, nuevo_valor):
        pedido = self._obtener_modificable(id_pedido)
        if pedido is None:
            return False
        pedido.cliente = nuevo_valor
        return self._guardar()

    def modificar_detalle(self, id_pedido, nuevo_valor):
        pedido = self._obtener_modificable(id_pedido)
        if pedido is None:
            return False
        pedido.detalle = nuevo_valor
        return self._guardar()

    def modificar_total(self, id_pedido, nuevo_valor):
        pedido = self._obtener_modificable(id_pedido)
        if pedido is None:
            return False
        pedido.total = nuevo_valor
        return self._guardar()

    def modificar_direccion(self, id_pedido, nueva_direccion):
        pedido = self._obtener_modificable(id_pedido)
        if pedido is None or not isinstance(pedido, PedidoDelivery):
            return False
        pedido.direccion = nueva_direccion
        return self._guardar()

    def cambiar_estado(self, id_pedido, nuevo_estado):
        pedido = self._obtener_modificable(id_pedido)
        if pedido is None:
            return False
        pedido.estado = nuevo_estado
        return self._guardar()

    def _obtener_modificable(self, id_pedido):
        pedido = self.buscar_por_id(id_pedido)
        if pedido is None or pedido.cancelado:
            return None
        return pedido

    # ---------------- Baja logica ----------------
    def cancelar_pedido(self, id_pedido):
        pedido = self.buscar_por_id(id_pedido)
        if pedido is None or pedido.cancelado:
            return False
        pedido.cancelar()
        return self._guardar()
