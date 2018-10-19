from IO import *
from VerPerfil import MenuVerPerfil
from VerPublicacion import MenuVerPublicacion
from VerNotificacion import MenuVerNotificacion
from Contactos import MenuContactos
from Empresas import MenuEmpresas
def menuPrincipal(usuario, conn):
    imprimir("BIENVENIDO " + usuario)
    imprimir("Que deseas hacer? \n"
             "\t(1) Ver Perfil\n"
             "\t(2) Ver Publicacion\n"
             "\t(3) Ver Notificacion\n"
             "\t(4) Contactos\n"
             "\t(5) Empresas\n")
    opcion = validar_opcion(range(1,6))

    if opcion ==1:
        MenuVerPerfil(usuario, conn)
    elif opcion == 2:
        MenuVerPublicacion(usuario, conn)
    elif opcion == 3:
        MenuVerNotificacion(usuario, conn)
    elif opcion == 4:
        MenuContactos(usuario, conn)
    elif opcion == 5:
        MenuEmpresas(usuario, conn)
    return