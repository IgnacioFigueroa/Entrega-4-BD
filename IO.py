def Imprimir(mensaje):
    print(mensaje)


def ImprimirError(mensaje):
    print(mensaje)

def ImprimirPositivo(mensaje):
    print(mensaje)

def ValidarOpcion(rango):
    opcion = int(input("Ingrese su opcion: "))
    while opcion not in rango:
        ImprimirError("Ingrese una opcion valida")
        opcion = int(input("Ingrese su opcion: "))
    return opcion