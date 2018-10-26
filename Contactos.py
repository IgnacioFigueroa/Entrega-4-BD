from IO import *
from tabulate import tabulate
from datetime import date
import psycopg2



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
VER_TRABAJOS = "SELECT e.nombre, t.descripcion, tr.fecha_inicio, tr.fecha_termino" \
               " FROM " \
               "Trabajo t JOIN Empresa e ON t.id_empresa = e.id " \
               "JOIN Trabajado tr ON t.id = tr.id_trabajo " \
               "JOIN Perfil p ON p.id = tr.id_perfil" \
               " WHERE p.correo_usuario = '{}'"
VER_ULTIMAS2_PUBLICACIONES = "SELECT texto, foto, link, fecha " \
                             "FROM Publicacion " \
                             "WHERE correo_usuario = '{}' AND borrada = false " \
                             "ORDER BY fecha DESC " \
                             "LIMIT 2"
VER_HABILIDADES = "SELECT h.nombre, COUNT(v.id_perfil_habilidad) " \
                  "FROM Habilidad h JOIN Perfil_habilidad pf ON h.id = pf.id_habilidad " \
                  "JOIN Perfil p ON p.id=pf.id_perfil " \
                  "LEFT JOIN Validacion v ON pf.id = v.id_perfil_habilidad " \
                  "WHERE p.correo_usuario = '{}' " \
                  "GROUP BY h.nombre"
VER_CONTACTOS_COMUNES = "SELECT amigo FROM {} contactos" \
                        " WHERE amigo in (SELECT amigo FROM {} contactos WHERE correo = '{}')" \
                        " AND amigo IN (SELECT amigo FROM {} contactos WHERE correo = '{}') "
VER_IDPERFILHABILIDAD = "SELECT pf.id " \
                        "FROM Habilidad h JOIN Perfil_habilidad pf ON h.id = pf.id_habilidad " \
                        "JOIN Perfil p ON p.id=pf.id_perfil " \
                        "LEFT JOIN Validacion v ON pf.id = v.id_perfil_habilidad " \
                        "WHERE p.correo_usuario = '{}' AND h.nombre = '{}'"
VER_IDVALIDACIONES = "SELECT id FROM Validacion"
VER_SOLICITUDESPENDIENTES = "SELECT * FROM Solicitud WHERE correo_usuario_receptor = '{}' AND estado = 'pendiente'"

# ---------------------------
def MenuContactos(usuario, conn):
    salir = False
    while (not salir):
        ImprimirTitulo("MENU DE CONTACTOS")
        Imprimir("Que deseas hacer? \n"
                 "\t(1) Ver Contactos\n"
                 "\t(2) Agregar Contactos\n"
                 "\t(3) Solicitudes Pendientes\n"
                 "\t(4) Salir\n")
        opcion = ValidarOpcion(range(1, 5))
        if opcion == 4:
            salir = False
        elif opcion == 1:
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
    opcion = ValidarOpcion(range(1, len(usuariosAmigos)+1))
    if opcion == 1:
        Imprimir("Selecciona el usuario del cual quieres ver su perfil\n")
        opcion = ValidarOpcion(range(1, selector + 1))
        amigoPorVer = usuariosAmigos[opcion - 1][0]
        VerPerfilHastaHabilidad(amigoPorVer, conn)

        cur.execute(VER_ULTIMAS2_PUBLICACIONES.format(amigoPorVer))
        publicaciones = cur.fetchall()
        tablaPublicaciones = list()
        atributosPublicacion = ["Texto", "Foto", "Link", "Fecha de Creacion"]
        Imprimir("ULTIMAS 2 PUBLICACIONES")
        for publicacion in publicaciones:
            for i in range(len(publicacion)):
                tablaPublicaciones.append([atributosPublicacion[i], publicacion[i]])
            Imprimir(tabulate(tablaPublicaciones))
            tablaPublicaciones = list()
        if len(publicaciones) == 1:
            Imprimir("El usuario solamente tiene 1 publicacion")

        cur.execute(
            VER_CONTACTOS_COMUNES.format(CONTACTOS_USUARIO, CONTACTOS_USUARIO, usuario, CONTACTOS_USUARIO, amigoPorVer))
        amigos = cur.fetchall()
        amigosEnComun = list()
        for amigo in amigos:
            if amigo not in amigosEnComun:
                amigosEnComun.append(amigo)
        Imprimir("Tienes {} amigos en comun con {}".format(len(amigosEnComun), amigoPorVer))
        Imprimir("Que deseas hacer: "
                 "(1) Validar Habilidad\n"
                 "(2) Volver")
        opcion = ValidarOpcion(range(1, 3))
        if opcion == 1:
            ValidarHabilidad(usuario, amigoPorVer, conn)
    if opcion == 2:
        Imprimir("Seleccione a quien desea elminar de su lista de amigos\n")
        opcion = ValidarOpcion(range(1, selector + 1))
        amigoPorEliminar = usuariosAmigos[opcion - 1][0]
        cur.execute("UPDATE Solicitud"
                    " SET estado = 'eliminada'"
                    " WHERE (correo_usuario_emisor = '{}' AND correo_usuario_receptor = '{}') "
                    "OR (correo_usuario_emisor = '{}' AND correo_usuario_receptor = '{}')".format(usuario,
                                                                                                  amigoPorEliminar,
                                                                                                  amigoPorEliminar,
                                                                                                    usuario))

        conn.commit()
        ImprimirPositivo("Usuario Eliminado")
        cur.close()
    return


def ValidarHabilidad(usuario, amigo, conn):
    cur = conn.cursor()
    cur.execute(VER_HABILIDADES.format(amigo))
    habilidades = cur.fetchall()
    contador = 1
    Imprimir("Que habilidad desea validar")
    for habilidad, validaciones in habilidades:
        Imprimir("\t({}) {}".format(contador, habilidad))
        contador += 1
    opcion = ValidarOpcion(range(1, len(habilidades) + 1))
    cur.execute(VER_IDVALIDACIONES)
    validaciones = cur.fetchall()
    idValidaciones = list()
    for i in validaciones:
        idValidaciones.append(i[0])
    cur.execute(VER_IDPERFILHABILIDAD.format(amigo, habilidades[opcion-1][0]))
    rows = cur.fetchall()
    idPerfilH = rows[0][0]
    cur.execute("INSERT INTO Validacion(id, correo_usuario_calificador, id_perfil_habilidad)"
                "VALUES ({},'{}',{})".format(max(idValidaciones) + 1, usuario, idPerfilH))
    cur.execute("INSERT INTO Notificacion(id, correo_usuario_notificado, id_validacion, leida) "
                "VALUES ({}, '{}', {}, {})".format(SiguienteID("Notificacion", conn),amigo, SiguienteID("Notificacion", conn, "id_validacion"),False))
    ImprimirPositivo("Habilidad Validada")
    ImprimirPositivo("Notificacion Enviada")
    conn.commit()
    cur.close()
    return


def AgregarContactos(usuario, conn):
    cur = conn.cursor()
    cur.execute("SELECT correo FROM Usuario WHERE correo NOT IN (SELECT amigo FROM {} contactos WHERE correo = '{}')".format(CONTACTOS_USUARIO, usuario))
    usuariosNoAmigos = cur.fetchall()
    selector = 0
    for user in usuariosNoAmigos:
        selector += 1
        Imprimir("({}) {}".format(selector, user[0]))
    Imprimir("Seleccione a que usuario desea agregar")
    opcion = ValidarOpcion(range(1,len(usuariosNoAmigos)+1))
    futuroAmigo = usuariosNoAmigos[opcion - 1][0]
    idSolicitud=SiguienteID("Solicitud", conn)
    cur.execute("INSERT INTO Solicitud(id, correo_usuario_emisor, correo_usuario_receptor, estado, fecha)"
                "VALUES ({}, '{}', '{}', '{}', '{}')".format(idSolicitud, usuario, futuroAmigo, "pendiente", date.today()))
    cur.execute("INSERT INTO Notificacion(id, correo_usuario_notificado, id_solicitud, leida)"
                "VALUES ({}, '{}', {}, {})".format(SiguienteID("Notificacion", conn),SiguienteID("Notificacion", conn, "id_solicitud"), futuroAmigo, False))
    conn.commit()
    cur.close()
    return

def SolicitudesPendientes(usuario, conn):
    cur=conn.cursor()
    cur.execute(VER_SOLICITUDESPENDIENTES.format(usuario))
    solicitudesPendientes= cur.fetchall()
    selector = 0
    if len(solicitudesPendientes) == 0:
        Imprimir("No hay solicitudes pendientes")
        return
    for solicitud in solicitudesPendientes:
        selector += 1
        Imprimir("({}) {}".format(selector, solicitud[1]))

    opcion = ValidarOpcion(range(1,len(solicitudesPendientes)), "Seleccione su solicitud pendiente")
    idSolicitud = solicitudesPendientes[opcion-1][0]
    Imprimir("Que desea hacer con la solicitud: \n"
             "(1) Aceptarla\n"
             "(2) Rechazarla\n"
             "(3) No hacer nada")
    opcion = ValidarOpcion(range(1,4))
    if opcion == 1:
        cur.execute("UPDATE Solicitud SET estado = 'aceptada' WHERE id = {}".format(idSolicitud))
        ImprimirPositivo("Solicitud aceptada")
    elif opcion == 2:
        cur.execute("UPDATE Solicitud SET estado = 'rechazada' WHERE id = {}".format(idSolicitud))
        ImprimirPositivo("Solicitud rechazada")
    else:
        cur.close()
        conn.commit()
        return
    cur.close()
    conn.commit()
    return

