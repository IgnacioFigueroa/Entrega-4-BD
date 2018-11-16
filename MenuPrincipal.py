from VerPerfil import MenuVerPerfil
from VerPublicacion import MenuVerPublicacion
from VerNotificacion import MenuVerNotificacion
from Contactos import MenuContactos
from Empresas import MenuEmpresas
from IO import *
from CrearCuenta import CrearCuenta
from RecuperarContraseña import RecuperarContrasena
from IniciarSesion import IniciarSesion
from MenuEstadisticas import MenuEstadisticas


def MenuPrincipal(usuario, conn):
    salir = True
    while(salir):
        ImprimirTitulo("BIENVENIDO " + usuario)
        Imprimir("Que deseas hacer? \n"
                 "\t(1) Ver Perfil\n"
                 "\t(2) Ver Publicacion\n"
                 "\t(3) Ver Notificacion\n"
                 "\t(4) Contactos\n"
                 "\t(5) Empresas\n"
                 "\t(6) Cerrar Sesion\n"
                 "\t(7) Ver Estadisticas\n"
                 "\t(8) Salir\n")
        opcion = ValidarOpcion(range(1, 9))
        if opcion == 1:
            MenuVerPerfil(usuario, conn)
        elif opcion == 2:
            MenuVerPublicacion(usuario, conn)
        elif opcion == 3:
            MenuVerNotificacion(usuario, conn)
        elif opcion == 4:
            MenuContactos(usuario, conn)
        elif opcion == 5:
            MenuEmpresas(usuario, conn)
        elif opcion == 6:
            salir = False
        elif opcion == 7:
            MenuEstadisticas(usuario, conn)
        elif opcion == 8:
            sys.exit(0)

    return