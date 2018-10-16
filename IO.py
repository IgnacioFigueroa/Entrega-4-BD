def imprimir(mensaje):
    print(mensaje)


def imprimir_error(mensaje):
    print(mensaje)

def imprimir_positivo(mensaje):
    print(mensaje)

def validar_opcion(rango):
    opcion = int(input("Ingrese su opcion: "))
    while opcion not in rango:
        imprimir_error("Ingrese una opcion valida")
        opcion = int(input("Ingrese su opcion: "))
    return opcion