from IO import *

def MenuVerPublicacion(usuario, conn):
    while True:
        ImprimirTitulo("ver publicaciones")
        Imprimir("Que desea hacer?\n"
                 "\t(1) Crear Publicacion\n"
                 "\t(2) Mis Publicaciones\n"
                 "\t(3) Otras Publicaciones\n"
                 "\t(4) Volver al menu anterior\n"
                 "\t(5) Salir\n")
        opcion = ValidarOpcion(range(1, 6))
        if opcion == 5:
            if HayConexionBD(conn):
                conn.close()
            sys.exit(0)
        elif opcion == 4:
            return
    return