from IO import *
def MenuEstadisticas(usuario, conn):
    Imprimir("Que desea hacer?"
             "\t (1) Ver calidad de contactos"
             "\t (2) Ver cantidad de comentarios")
    opcion = ValidarOpcion(range(1,3))
    if opcion == 1:
        CalidadContactos(usuario, conn)
    elif opcion == 2:
        CantidadComentarios(usuario, conn)
    return


def CalidadContactos(usuario, conn):
    return
def CantidadComentarios(usuario, conn):
    return