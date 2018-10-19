from IO import *
def MenuContactos(usuario, conn):
    Imprimir("MENU DE CONTACTOS")
    Imprimir("Que deseas hacer? \n"
             "\t(1) Ver Contactos\n"
             "\t(2) Agregar Contactos\n"
             "\t(3) Solicitudes Pendientes\n")
    opcion = ValidarOpcion(1,4)
    if opcion == 1:
        VerContactos(usuario, conn)
    elif opcion == 2:
        AgregarContactos(usuario, conn)
    elif opcion == 3:
        SolicitudesPendientes(usuario, conn)

    return

def VerContactos(usuario, conn):
    return
def AgregarContactos(usuario, conn):
    return
def SolicitudesPendientes(usuario, conn):
    return
