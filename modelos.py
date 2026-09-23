from abc import ABC, abstractmethod
from datetime import datetime


class Pedido(ABC):

    ESTADOS_VALIDOS = ('Pendiente', 'Entregado', 'Cancelado')

    def __init__(self, id_pedido, cliente, detalle, total):
        self._id = id_pedido
        self._cliente = None
        self._detalle = None
        self._total = None
        self._estado = 'Pendiente'
        self._cancelado = False
        self._fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Usamos los setters para que validen desde el momento de la creacion
        self.cliente = cliente
        self.detalle = detalle
        self.total = total

    # ---------------- Encapsulamiento: propiedades con validacion ----------------
    @property
    def id(self):
        return self._id

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError('El nombre del cliente es obligatorio.')
        self._cliente = valor.strip()

    @property
    def detalle(self):
        return self._detalle

    @detalle.setter
    def detalle(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError('El detalle del pedido es obligatorio.')
        self._detalle = valor.strip()

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValueError('El total debe ser un numero (ej: 1500 o 1500.50).')
        if valor <= 0:
            raise ValueError('El total debe ser mayor a $0.')
        self._total = valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f'Estado invalido. Debe ser uno de {self.ESTADOS_VALIDOS}')
        self._estado = valor

    @property
    def cancelado(self):
        return self._cancelado

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    def cancelar(self):
        self._cancelado = True
        self._estado = 'Cancelado'

    def marcar_entregado(self):
        self._estado = 'Entregado'

    # ---------------- Abstraccion: contrato que cada subclase debe cumplir ----------------
    @abstractmethod
    def calcular_costo_envio(self):
        raise NotImplementedError

    @abstractmethod
    def obtener_tipo(self):
        raise NotImplementedError

    # ---------------- Polimorfismo ----------------
    def calcular_total_final(self):
        return round(self.total + self.calcular_costo_envio(), 2)

    def mostrar_resumen(self):
        return (
            f'ID: {self.id:<4} | Tipo: {self.obtener_tipo():<16} | '
            f'Cliente: {self.cliente:<20} | Total: ${self.calcular_total_final():>8.2f} '
            f'| Estado: {self.estado}'
        )

    def to_dict(self):
        return {
            'tipo': self.obtener_tipo_clave(),
            'id': self._id,
            'cliente': self._cliente,
            'detalle': self._detalle,
            'total': self._total,
            'estado': self._estado,
            'cancelado': self._cancelado,
            'fecha_creacion': self._fecha_creacion,
        }

    def obtener_tipo_clave(self):
        return type(self).__name__

    def __str__(self):
        return self.mostrar_resumen()


class PedidoDelivery(Pedido):

    COSTO_ENVIO_BASE = 500.0

    def __init__(self, id_pedido, cliente, detalle, total, direccion):
        super().__init__(id_pedido, cliente, detalle, total)
        self._direccion = None
        self.direccion = direccion

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError('La direccion de entrega es obligatoria.')
        self._direccion = valor.strip()

    def calcular_costo_envio(self):
        return self.COSTO_ENVIO_BASE

    def obtener_tipo(self):
        return 'Delivery'

    def mostrar_resumen(self):
        base = super().mostrar_resumen()
        return f'{base}\n      Direccion: {self.direccion} | Detalle: {self.detalle}'

    def to_dict(self):
        data = super().to_dict()
        data['direccion'] = self._direccion
        return data


class PedidoRetiro(Pedido):

    def calcular_costo_envio(self):
        return 0.0

    def obtener_tipo(self):
        return 'Retiro en local'

    def mostrar_resumen(self):
        base = super().mostrar_resumen()
        return f'{base}\n      (Retira en local) | Detalle: {self.detalle}'
