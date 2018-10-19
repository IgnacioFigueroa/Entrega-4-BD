
def Imprimir(mensaje):
    print(mensaje)

def ImprimirTitulo(titulo):
    linea = "     "
    for i in range(len(titulo)):
        linea = linea + "_"
    print(linea)
    print("     " + titulo)
    print()

def ImprimirError(mensaje):
    print(mensaje)

def ImprimirPositivo(mensaje):
    print(mensaje)

def ValidarOpcion(rango, mensaje = "Ingrese su opcion: "):
    opcion = input(mensaje)
    patron = []
    for a in rango:
        patron.append(str(a))
    while not (opcion in patron):
        ImprimirError("Ingrese una opcion valida")
        opcion = input(mensaje)
    return int(opcion)


