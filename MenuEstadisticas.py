from IO import *
import psycopg2
from matplotlib import pyplot
from datetime import datetime
import numpy


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
                    "WHERE todos.correo = '{}'" \
                    'ORDER BY todos.correo DESC)'

CONTACTOS_USUARIO2 = '(SELECT todos.amigo amigo' \
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

CANTIDAD_TRABAJOS = "SELECT p.correo_usuario, count(*)c FROM Trabajado t JOIN Perfil p ON p.id = t.id_perfil WHERE p.correo_usuario = '{}' GROUP BY p.correo_usuario"
DIAS_TRABAJADOS = " SELECT count(*),sum(" \
                  "CASE WHEN (fecha_termino>'31-12-{}' or fecha_termino is null) and '31-12-{}'>fecha_inicio THEN ('31-12-{}'-fecha_inicio) " \
                  "ELSE (fecha_termino-fecha_inicio) END) " \
                  "FROM Trabajado t JOIN Perfil p ON p.id = t.id_perfil " \
                  "WHERE p.correo_usuario = '{}'"

ANO_INICIO = "select extract(year from fecha_inicio) inicio " \
             "from trabajado t join perfil p on t.id_perfil = p.id " \
             "WHERE correo_usuario = '{}' " \
             "order by inicio asc limit 1"

ANO_FIN = "select extract(year from fecha_termino) fin " \
             "from trabajado t join perfil p on t.id_perfil = p.id " \
             "WHERE correo_usuario = '{}' " \
             "order by fin desc limit 1"
#conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")
#u = "Mono3Apellido3@gmail.com"

def MenuEstadisticas(usuario, conn):
    salir = False
    while (not salir):
        Imprimir("Que desea hacer?\n"
                 "\t (1) Ver calidad de contactos\n"
                 "\t (2) Ver cantidad de comentarios\n"
                 "\t (3) Ver trabajos\n"
                 "\t (4) Ver habilidades\n"
                 "\t (5) Ver tus trabajos\n"
                 "\t (6) Volver\n"
                 "\t (7) Salir")
        opcion = ValidarOpcion(range(1,8))
        if opcion == 1:
            CalidadContactos(usuario, conn)
        elif opcion == 2:
            CantidadComentarios(usuario, conn)
        elif opcion == 3:
            Trabajos(usuario, conn)
        elif opcion == 4:
            Habilidades(usuario, conn)
        elif opcion == 5:
            TusTrabajos(usuario, conn)
        elif opcion == 6:
            salir = True
        elif opcion == 7:
            conn.close()
            sys.exit(0)
    return


def CalidadContactos(usuario, conn):
    cur = conn.cursor()
    cur.execute(VER_CONTACTOS_ESTUDIO.format(CONTACTOS_USUARIO.format(usuario), usuario))
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
    cur.execute(VER_HABILIDADES2.format(CONTACTOS_USUARIO2.format(usuario)))
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
def TusTrabajos(usuario, conn):
    cur = conn.cursor()
    cur.execute(ANO_INICIO.format(usuario))
    a = cur.fetchall()
    ano_inicio = int(a[0][0])
    cur.execute(ANO_FIN.format(usuario))
    a=cur.fetchall()
    if a[0][0] is None:
        ano_fin = datetime.now().year
    else:
        ano_fin = a[0][0]
    datos = [numpy.array(range(ano_inicio,(ano_fin))), []]
    for ano in range(ano_inicio, ano_fin):
        cur.execute(DIAS_TRABAJADOS.format(str(ano),str(ano),str(ano),usuario))
        dias= cur.fetchall()
        promedio = round(float(dias[0][1])/float(dias[0][0]),2)
        datos[1].append(promedio)
    pyplot.plot(datos[0],datos[1])
    pyplot.xlabel("Años")
    pyplot.ylabel("Promedio de dias trabajados")
    pyplot.show()
    return

#MenuEstadisticas(u,conn)