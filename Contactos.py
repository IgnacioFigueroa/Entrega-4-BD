from IO import *
from tabulate import tabulate
import psycopg2

conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")

# ----------QUERYS----------
CONTACTOS_USUARIO = '(SELECT todos.correo correo, todos.amigo amigo' \
                    ' FROM ' \
                    '(SELECT u.correo correo, COUNT(*) amigos, ' \
                    ' CASE  WHEN u.correo = s.correo_usuario_emisor THEN s.correo_usuario_receptor ' \
                    'WHEN u.correo = s.correo_usuario_receptor THEN s.correo_usuario_emisor ' \
                    'END amigo ' \
                    'FROM ' \
                    'usuario u JOIN solicitud s ON (u.correo = s.correo_usuario_emisor OR u.correo = s.correo_usuario_receptor) ' \
                    'WHERE  s.estado = \'aceptada\' ' \
                    'GROUP BY u.correo, s.correo_usuario_receptor, s.correo_usuario_emisor ORDER BY amigos DESC) todos ' \
                    'ORDER BY todos.correo DESC)'
VER_PERFIL = "SELECT * FROM Perfil WHERE correo_usuario = '{}' "
VER_ESTUDIOS = "SELECT em.nombre, e.grado_academico, e.descripcion, e.fecha_inicio, e.fecha_termino " \
               "FROM Estudio e JOIN Empresa em ON e.id_empresa = em.id " \
               "WHERE correo_usuario = '{}'"


def MenuContactos(usuario, conn):
    salir = False
    while(not salir):
        ImprimirTitulo("MENU DE CONTACTOS")
        Imprimir("Que deseas hacer? \n"
                 "\t(1) Ver Contactos\n"
                 "\t(2) Agregar Contactos\n"
                 "\t(3) Solicitudes Pendientes\n"
                 "\t(4) Salir")
        opcion = ValidarOpcion(range(1, 4))
        if opcion == 1:
            VerContactos(usuario, conn)
        elif opcion == 2:
            AgregarContactos(usuario, conn)
        elif opcion == 3:
            SolicitudesPendientes(usuario, conn)
    return


def VerContactos(usuario, conn):
    cur = conn.cursor()
    cur.execute("SELECT amigo FROM {} contactos WHERE correo = '{}'".format(CONTACTOS_USUARIO, usuario))
    usuariosAmigos = cur.fetchall()
    selector = 0
    for amigo in usuariosAmigos:
        selector += 1
        Imprimir("({}) {}".format(selector, amigo[0]))
    Imprimir("Que deseas hacer? \n"
             "\t(1) Ver Perfil\n"
             "\t(2) Eliminar contacto\n")
    opcion = ValidarOpcion(range(1, 3))
    if opcion == 1:
        Imprimir("Selecciona el usuario del cual quieres ver su perfil\n")
        opcion = ValidarOpcion(range(1, selector + 1))
        amigoPorVer = usuariosAmigos[opcion - 1][0]
        cur.execute(VER_PERFIL.format(amigoPorVer))
        perfilPorVer = cur.fetchall()[0]
        atributosPerfil = ["Correo", "Nombre", "Apellido", "Fecha de Nacimiento", "Pais", "Sexo", "Descripcion"]
        tablaPerfil = list()
        for i in range(7):
            tablaPerfil.append([atributosPerfil[i], perfilPorVer[i + 1]])
        cur.execute(VER_ESTUDIOS.format(amigoPorVer))
        estudios = cur.fetchall()
        atributosEstudios = ["GradoAcademico, Descripcion, FechaInicio, FechaTermino"]
        Imprimir(tabulate(tablaPerfil))
        Imprimir(tabulate(estudios))

    return


def AgregarContactos(usuario, conn):
    return


def SolicitudesPendientes(usuario, conn):
    return


