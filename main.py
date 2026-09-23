from menu import MenuRoticeria


def main():
    app = MenuRoticeria(archivo_datos='pedidos.json')
    app.ejecutar()


if __name__ == '__main__':
    main()
