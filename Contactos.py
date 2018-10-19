from IO import *
#----------QUERYS----------
CONTACTOS_USUARIO = 'SELECT todos.correo correo, todos.amigo amigo' \
                    ' FROM ' \
                    '(SELECT u.correo correo, COUNT(*) amigos, ' \
                    ' CASE  WHEN u.correo = s.correo_usuario_emisor THEN s.correo_usuario_receptor ' \
                    'WHEN u.correo = s.correo_usuario_receptor THEN s.correo_usuario_emisor ' \
                    'END amigo ' \
                    'FROM ' \
                    'usuario u JOIN solicitud s ON (u.correo = s.correo_usuario_emisor OR u.correo = s.correo_usuario_receptor) ' \
                    'WHERE  s.estado = \'aceptada\' ' \
                    'GROUP BY u.correo, s.correo_usuario_receptor, s.correo_usuario_emisor ORDER BY amigos DESC) todos ' \
                    'ORDER BY todos.correo DESC'
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
