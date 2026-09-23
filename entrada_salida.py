"""
entrada_salida.py
------------------
Funciones auxiliares de consola. Equivalen a LeerReal() y a los distintos
'repeat...until' de validacion del Pascal original.
"""

import os


def leer_entero(mensaje, minimo=None):
    while True:
        entrada = input(mensaje)
        try:
            valor = int(entrada)
        except ValueError:
            print('ERROR: Ingrese solo numeros enteros.')
            continue
        if minimo is not None and valor < minimo:
            print(f'ERROR: Ingrese un numero mayor o igual a {minimo}.')
            continue
        return valor


def leer_real(mensaje):
    while True:
        entrada = input(mensaje)
        try:
            valor = float(entrada.replace(',', '.'))
        except ValueError:
            print('ERROR: Ingrese solo numeros (ej: 1500 o 1500.50).')
            continue
        if valor <= 0:
            print('ERROR: El total debe ser mayor a $0.')
            continue
        return valor


def leer_texto_obligatorio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print('ERROR: Este campo es obligatorio.')


def leer_si_no(mensaje):
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ('s', 'si'):
            return True
        if valor in ('n', 'no'):
            return False
        print('ERROR: Ingrese S, si, N o no.')


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input('Presione ENTER para volver al menu...')


def linea_separacion():
    print('-' * 55)
