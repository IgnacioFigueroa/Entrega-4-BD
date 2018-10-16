from api_clase import imprimir, validar_opcion


def menu_principal(usuario, conn):
    imprimir("BIENVENIDO " + usuario)
    imprimir("Que deseas hacer? \n"
             "\t(1) Ver Perfil\n"
             "\t(2) Ver Publicacion\n"
             "\t(3) Ver Notificacion\n"
             "\t(4) Contactos\n"
             "\t(5) Empresas\n")
    opcion = validar_opcion(range(1,6))

    return