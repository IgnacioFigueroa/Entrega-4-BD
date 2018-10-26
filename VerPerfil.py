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
VER_HABILIDADES = "SELECT h.id, h.nombre, COUNT(v.id_perfil_habilidad) " \
                  "FROM Habilidad h JOIN Perfil_habilidad pf ON h.id = pf.id_habilidad " \
                  "JOIN Perfil p ON p.id=pf.id_perfil " \
                  "LEFT JOIN Validacion v ON pf.id = v.id_perfil_habilidad " \
                  "WHERE p.correo_usuario = '{}' " \
                  "GROUP BY h.id"
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
def MenuVerPerfil(usuario, conn):
    VerPerfilHastaHabilidad(usuario, conn)
    return
#MenuVerPerfil("Mono1Apellido1@gmail.com", conn)

u = "Mono1Apellido1@gmail.com"

def VerHabilidades(usuario, conn):
    ImprimirTitulo("ver habilidades")
    cur = conn.cursor()
    cur.execute(VER_HABILIDADES.format(usuario))
    respuesta = cur.fetchall()
    matriz_mostrar = [["HABILIDAD", "DESCRIPCION", "CANTIDAD DE VALIDACIONES"]]
    ids = []
    for tupla in respuesta:
        ids.append(tupla[0])
        matriz_mostrar.append([tupla[0], tupla[1], tupla[2]])
    Imprimir(tabulate(matriz_mostrar))
    Imprimir("Que desea hacer?\n"
             "(1) Ver Habilidad\n"
             "(2) Agregar Habilidad\n"
             "(3) Eliminar Habilidad\n"
             "(4) Volver al menu anterior\n"
             "(5) Salir\n")
    opcion = ValidarOpcion(range(1,5))
    if opcion == 1:
        habilidad_seleccionada = ValidarOpcion(ids, "Seleccione la habilidad que quiere ver: ")
        cur.execute("select h.id, v.id, v.correo_usuario_calificador "
                    "from habilidad h, perfil_habilidad ph, validacion v, perfil p "
                    "where h.id = ph.id_habilidad and ph.id = v.id_perfil_habilidad "
                    "and p.id = ph.id_perfil and h.id = {} and p.correo_usuario = '{}'"
                    .format(habilidad_seleccionada, usuario))
        respuesta = cur.fetchall()
        if len(respuesta) > 0:
            matriz_mostrar = [["HABILIDAD", "VALIDACION", "VALIDADA POR"]]
            for tupla in respuesta:
                matriz_mostrar.append([tupla[0], tupla[1], tupla[2]])
            Imprimir(tabulate(matriz_mostrar))
        else:
            Imprimir("La habilidad seleccionada no tiene validaciones")
    elif opcion == 2:
        pass
    cur.close()

VerHabilidades(u, conn)