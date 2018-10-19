import re
def Imprimir(mensaje):
    print(mensaje)


def ImprimirError(mensaje):
    print(mensaje)

def ImprimirPositivo(mensaje):
    print(mensaje)

def ValidarOpcion(rango):
    opcion = input("Ingrese su opcion: ")
    patron = "[{}-{}]".format(rango[0],rango[-1])
    while not re.match(patron, opcion):
        ImprimirError("Ingrese una opcion valida")
        opcion = input("Ingrese su opcion: ")
    return int(opcion)