from IO import *
import psycopg2
from matplotlib import pyplot

CONTACTOS_USUARIO = '(SELECT todos.amigo amigo' \
                    ' FROM ' \
                    '(SELECT u.correo correo, COUNT(*) amigos, ' \
                    ' CASE  WHEN u.correo = s.correo_usuario_emisor THEN s.correo_usuario_receptor ' \
                    'WHEN u.correo = s.correo_usuario_receptor THEN s.correo_usuario_emisor ' \
                    'END amigo ' \
                    'FROM ' \
                    'usuario u JOIN solicitud s ON (u.correo = s.correo_usuario_emisor OR u.correo = s.correo_usuario_receptor) ' \
                    'WHERE  s.estado = \'aceptada\' ' \
                    'GROUP BY u.correo, s.correo_usuario_receptor, s.correo_usuario_emisor ORDER BY amigos DESC) todos ' \
                    "WHERE todos.correo = '{}'" \
                    'ORDER BY todos.correo DESC)'

VER_CONTACTOS_ESTUDIO = "SELECT cu.amigo, e.grado_academico FROM {} cu JOIN Estudio e ON e.correo_usuario = cu.correo WHERE cu.correo = '{}' "

COOMENTARIOS_POR_MES = "select count(*) cantidad_comentarios, extract(month from c.fecha) "\
                "from comentario c left join publicacion p on p.id = c.id_publicacion "\
                "where c.correo_usuario_comentador = '{}' or p.correo_usuario = '{}' "\
                "group by extract(month from c.fecha)"

TRABAJOS_DISPONIBLES_RUBRO = "select e.rubro, count(*) cantidad_trabajos from Empresa e, Trabajo t "\
                "where t.id_empresa = e.id and t.postulacion_abierta is True group by e.rubro"

VER_HABILIDADES = "SELECT h.nombre, COUNT(v.id_perfil_habilidad) " \
                  "FROM Habilidad h JOIN Perfil_habilidad pf ON h.id = pf.id_habilidad " \
                  "JOIN Perfil p ON p.id=pf.id_perfil " \
                  "LEFT JOIN Validacion v ON pf.id = v.id_perfil_habilidad " \
                  "WHERE p.correo_usuario = '{}' " \
                  "GROUP BY h.id"

VER_HABILIDADES2 = "SELECT h.nombre, COUNT(v.id_perfil_habilidad) " \
                  "FROM Habilidad h JOIN Perfil_habilidad pf ON h.id = pf.id_habilidad " \
                  "JOIN Perfil p ON p.id=pf.id_perfil " \
                  "LEFT JOIN Validacion v ON pf.id = v.id_perfil_habilidad " \
                  "WHERE p.correo_usuario IN {} " \
                  "GROUP BY p.correo_usuario, h.id " \
                  "ORDER BY COUNT(v.id_perfil_habilidad) DESC LIMIT 10"

#conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")
#u = "Mono3Apellido3@gmail.com"

def MenuEstadisticas(usuario, conn):
    Imprimir("Que desea hacer?\n"
             "\t (1) Ver calidad de contactos\n"
             "\t (2) Ver cantidad de comentarios\n"
             "\t (3) Ver trabajos\n"
             "\t (4) Ver habilidades\n")
    opcion = ValidarOpcion(range(1,5))
    if opcion == 1:
        CalidadContactos(usuario, conn)
    elif opcion == 2:
        CantidadComentarios(usuario, conn)
    elif opcion == 3:
        Trabajos(usuario, conn)
    elif opcion == 4:
        Habilidades(usuario, conn)
    return


def CalidadContactos(usuario, conn):
    cur = conn.cursor()
    cur.execute(VER_CONTACTOS_ESTUDIO.format(CONTACTOS_USUARIO, usuario))
    rows = cur.fetchall()
    lista = []
    for correo, grado in rows:
        lista.append(grado)
    pyplot.hist(lista)
    pyplot.show()
    return

def CantidadComentarios(usuario, conn):
    cur = conn.cursor()
    cur.execute(COOMENTARIOS_POR_MES.format(usuario, usuario))
    resultado = cur.fetchall()
    cantidades = [0,0,0,0,0,0,0,0,0,0,0,0]
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril',
             'Mayo', 'Junio', 'Julio', 'Agosto',
             'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    for tupla in resultado:
        cantidades[int(tupla[1])-1] = tupla[0]

    pyplot.plot(meses, cantidades)
    pyplot.xlabel("Meses")
    pyplot.ylabel("Cantidad comentarios")
    pyplot.show()
    return

def Trabajos(usuario, conn):
    cur = conn.cursor()
    cur.execute(TRABAJOS_DISPONIBLES_RUBRO)
    rubros = cur.fetchall()
    lista_rubros = []
    lista_cantidades = []
    for r in rubros:
        lista_rubros.append(r[0])
        lista_cantidades.append(r[1])
    pyplot.bar(lista_rubros, lista_cantidades)
    pyplot.xlabel("Rubros")
    pyplot.ylabel("Cantidad trabajos disponibles")
    pyplot.show()
    return

def Habilidades(usuario, conn):
    cur = conn.cursor()
    cur.execute(VER_HABILIDADES2.format(CONTACTOS_USUARIO.format(usuario)))
    hb = cur.fetchall()
    numeros = []
    habis = []
    for h in hb:
        numeros.append(h[1])
        habis.append(h[0])

    pyplot.bar(habis, numeros)
    pyplot.xlabel("Habilidades")
    pyplot.ylabel("Cantidad validaciones")
    pyplot.show()
    return
