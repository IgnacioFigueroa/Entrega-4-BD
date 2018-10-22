import sys

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

def ImprimirOpciones(listaOpciones, titulo = ""):
    i = 1
    stringOpciones = titulo
    for a in listaOpciones:
        stringOpciones += "\n({}) {}.".format(i,a)
        i += 1
    print (stringOpciones)

def PedirDescripcion(arg = "descripcion"):
    Imprimir("Ingrese {}. Use doble espacio para terminar".format(arg))
    texto = ""
    n_text = " "
    while len(n_text) != 0:
        n_text = input()
        texto += n_text
    return texto