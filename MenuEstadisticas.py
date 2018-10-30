from IO import *
import psycopg2
from matplotlib import pyplot

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

VER_CONTACTOS_ESTUDIO = "SELECT cu.amigo, e.grado_academico FROM {} cu JOIN Estudio e ON e.correo_usuario = cu.correo WHERE cu.correo = '{}' "
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")
def MenuEstadisticas(usuario, conn):
    Imprimir("Que desea hacer?\n"
             "\t (1) Ver calidad de contactos\n"
             "\t (2) Ver cantidad de comentarios\n")
    opcion = ValidarOpcion(range(1,3))
    if opcion == 1:
        CalidadContactos(usuario, conn)
    elif opcion == 2:
        CantidadComentarios(usuario, conn)
    return


def CalidadContactos(usuario, conn):
    cur = conn.cursor()
    cur.execute(VER_CONTACTOS_ESTUDIO.format(CONTACTOS_USUARIO, usuario))
    rows = cur.fetchall()
    lista = []
    for correo, grado in rows:
        lista.append(grado)
    print(rows)
    cols = []
    vals = []
    pyplot.hist(lista)
    pyplot.show()
    return

from matplotlib import pyplot
def CantidadComentarios(usuario, conn):
    cur = conn.cursor()
    cur.execute("select count(*) cantidad_comentarios, extract(month from c.fecha) "
                "from comentario c left join publicacion p on p.id = c.id_publicacion "
                "where c.correo_usuario_comentador = '{}' or p.correo_usuario = '{}' "
                "group by extract(month from c.fecha)".format(usuario, usuario))
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

