from IO import *
def MenuEstadisticas(usuario, conn):
    Imprimir("Que desea hacer?"
             "\t (1) Ver calidad de contactos"
             "\t (2) Ver cantidad de comentarios")
    opcion = ValidarOpcion(range(1,3))
    if opcion == 1:
        CalidadContactos(usuario, conn)
    elif opcion == 2:
        CantidadComentarios(usuario, conn)
    return


def CalidadContactos(usuario, conn):
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
    pyplot.show()
    return

