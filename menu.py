"""
menu.py
-------
Interfaz de consola. Equivale a MostrarMenu + los procedimientos de cada
opcion del Pascal original, pero aca SOLO se encarga de mostrar texto y
pedir datos: toda la logica real vive en GestorPedidos (separacion de
responsabilidades).
"""

from entrada_salida import (
    leer_entero,
    leer_real,
    leer_texto_obligatorio,
    leer_si_no,
    limpiar_pantalla,
    pausar,
    linea_separacion,
)
from gestor_pedidos import GestorPedidos
from modelos import PedidoDelivery


class MenuRoticeria:
    """Ciclo principal del sistema de pedidos."""

    def __init__(self, archivo_datos='pedidos.json'):
        self._archivo_datos = archivo_datos
        self._gestor = GestorPedidos(repositorio=self._crear_repositorio())

    def _crear_repositorio(self):
        from repositorio import RepositorioJSON
        return RepositorioJSON(self._archivo_datos)

    def _recargar_datos(self):
        """Relee el JSON, igual que el Pascal hacia CargarDesdeDisco antes de operar."""
        self._gestor = GestorPedidos(repositorio=self._crear_repositorio())

    def mostrar_menu(self):
        limpiar_pantalla()
        print('=' * 51)
        print('      SISTEMA DE PEDIDOS - ROTICERIA          ')
        print('=' * 51)
        print('   1. Cargar nuevo pedido')
        print('   2. Consultar pedido por ID')
        print('   3. Listar pedidos pendientes')
        print('   4. Listar todos los pedidos')
        print('   5. Modificar pedido')
        print('   6. Cancelar pedido')
        print('   0. Salir')
        print('=' * 51)

    def ejecutar(self):
        acciones = {
            1: self.cargar_pedido,
            2: self.consultar_pedido,
            3: self.listar_pendientes,
            4: self.listar_todos,
            5: self.modificar_pedido,
            6: self.cancelar_pedido,
        }
        opcion = -1
        while opcion != 0:
            self.mostrar_menu()
            opcion = leer_entero('Opcion: ')
            if opcion == 0:
                print('Chauuu')
            elif opcion in acciones:
                acciones[opcion]()
            else:
                print('Opcion invalida. Ingrese un numero del 0 al 6.')
                pausar()

    # ---------------- Opcion 1 ----------------
    def cargar_pedido(self):
        continuar = True
        while continuar:
            limpiar_pantalla()
            print('=== CARGAR PEDIDO ===')

            print('Tipo de pedido:')
            print('  1. Delivery (con envio a domicilio)')
            print('  2. Retiro en local')
            tipo = leer_entero('Opcion: ')
            while tipo not in (1, 2):
                print('ERROR: Ingrese 1 o 2.')
                tipo = leer_entero('Opcion: ')

            cliente = leer_texto_obligatorio('Nombre del cliente: ')
            detalle = leer_texto_obligatorio('Detalle del pedido (ej: 1 pollo, 2 empanadas): ')
            total = leer_real('Total a cobrar ($): ')

            if tipo == 1:
                direccion = leer_texto_obligatorio('Direccion de entrega: ')
                nuevo = self._gestor.crear_pedido_delivery(cliente, detalle, total, direccion)
            else:
                nuevo = self._gestor.crear_pedido_retiro(cliente, detalle, total)

            print(f'Pedido #{nuevo.id} ({nuevo.obtener_tipo()}) cargado correctamente.')
            linea_separacion()

            continuar = leer_si_no('Desea cargar otro pedido? (S/N): ')

        pausar()

    # ---------------- Opcion 2 ----------------
    def consultar_pedido(self):
        limpiar_pantalla()
        print('=== CONSULTAR PEDIDO ===')
        id_buscado = leer_entero('Ingrese el ID del pedido a buscar: ')

        self._recargar_datos()
        pedido = self._gestor.buscar_por_id(id_buscado)

        if pedido is None:
            print(f'No se encontro ningun pedido con el ID: {id_buscado}')
        elif pedido.cancelado:
            print(f'El pedido #{id_buscado} fue CANCELADO y no esta disponible.')
        else:
            print('----------- PEDIDO ENCONTRADO -----------')
            print(pedido.mostrar_resumen())
            linea_separacion()

        pausar()

    # ---------------- Opcion 3 ----------------
    def listar_pendientes(self):
        limpiar_pantalla()
        self._recargar_datos()
        pendientes = self._gestor.listar_pendientes()

        print('============== PEDIDOS PENDIENTES ==============')
        if not pendientes:
            print('No hay pedidos pendientes.')
        else:
            for pedido in pendientes:
                print(pedido.mostrar_resumen())
                linea_separacion()

        pausar()

    # ---------------- Opcion 4 ----------------
    def listar_todos(self):
        limpiar_pantalla()
        self._recargar_datos()

        print('============== PEDIDOS PENDIENTES ==============')
        pendientes = self._gestor.listar_pendientes()
        if not pendientes:
            print('  (Sin pedidos pendientes)')
        else:
            for pedido in pendientes:
                print(pedido.mostrar_resumen())
                linea_separacion()

        print()
        print('============== PEDIDOS ENTREGADOS ==============')
        entregados = self._gestor.listar_entregados()
        if not entregados:
            print('  (Sin pedidos entregados)')
        else:
            for pedido in entregados:
                print(pedido.mostrar_resumen())
                linea_separacion()

        pausar()

    # ---------------- Opcion 5 ----------------
    def modificar_pedido(self):
        limpiar_pantalla()
        print('=== MODIFICAR PEDIDO ===')
        self._recargar_datos()

        id_buscado = leer_entero('Ingrese el ID del pedido a modificar: ')
        pedido = self._gestor.buscar_por_id(id_buscado)

        if pedido is None:
            print(f'No se encontro el pedido con ID: {id_buscado}')
            pausar()
            return

        if pedido.cancelado:
            print(f'El pedido #{id_buscado} fue cancelado y no puede modificarse.')
            pausar()
            return

        es_delivery = isinstance(pedido, PedidoDelivery)

        print(f'--- Datos actuales del pedido #{id_buscado} ---')
        print(f'1. Cliente   : {pedido.cliente}')
        if es_delivery:
            print(f'2. Direccion : {pedido.direccion}')
        print(f'3. Detalle   : {pedido.detalle}')
        print(f'4. Total     : ${pedido.total:.2f}')
        print(f'5. Estado    : {pedido.estado}')

        campo = leer_entero('Que campo desea modificar? (1-5): ')

        if campo == 1:
            nuevo = leer_texto_obligatorio('Nuevo nombre del cliente: ')
            self._gestor.modificar_cliente(id_buscado, nuevo)
        elif campo == 2:
            if es_delivery:
                nueva = leer_texto_obligatorio('Nueva direccion: ')
                self._gestor.modificar_direccion(id_buscado, nueva)
            else:
                print('Este pedido es "Retiro en local", no tiene direccion.')
        elif campo == 3:
            nuevo = leer_texto_obligatorio('Nuevo detalle del pedido: ')
            self._gestor.modificar_detalle(id_buscado, nuevo)
        elif campo == 4:
            nuevo = leer_real('Nuevo total ($): ')
            self._gestor.modificar_total(id_buscado, nuevo)
        elif campo == 5:
            print('Seleccione el nuevo estado:')
            print('  1. Pendiente')
            print('  2. Entregado')
            opcion_estado = leer_entero('Opcion: ')
            if opcion_estado == 1:
                self._gestor.cambiar_estado(id_buscado, 'Pendiente')
            elif opcion_estado == 2:
                self._gestor.cambiar_estado(id_buscado, 'Entregado')
            else:
                print('Opcion invalida, no se cambio el estado.')
        else:
            print('Opcion invalida.')
            pausar()
            return

        print(f'Pedido #{id_buscado} modificado correctamente.')
        pausar()

    # ---------------- Opcion 6 ----------------
    def cancelar_pedido(self):
        limpiar_pantalla()
        print('=== CANCELAR PEDIDO ===')
        self._recargar_datos()

        id_buscado = leer_entero('Ingrese el ID del pedido a cancelar: ')
        pedido = self._gestor.buscar_por_id(id_buscado)

        if pedido is None:
            print(f'No se encontro el pedido con ID: {id_buscado}')
            pausar()
            return

        if pedido.cancelado:
            print(f'El pedido #{id_buscado} ya estaba cancelado.')
            pausar()
            return

        print('--- Pedido a cancelar ---')
        print(pedido.mostrar_resumen())
        linea_separacion()

        confirmar = leer_si_no('Esta seguro que desea CANCELAR este pedido? (S/N): ')
        if confirmar:
            self._gestor.cancelar_pedido(id_buscado)
            print(f'Pedido #{id_buscado} cancelado correctamente.')
        else:
            print('Operacion abortada. El pedido no fue modificado.')

        pausar()
