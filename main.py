"""
main.py
-------
Punto de entrada del programa. Simplemente importa el menu y lo arranca,
igual que el 'begin ... end.' principal del Pascal original.
"""

from menu import MenuRoticeria


def main():
    app = MenuRoticeria(archivo_datos='pedidos.json')
    app.ejecutar()


if __name__ == '__main__':
    main()
