from IO import *
import datetime

import psycopg2
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")


crearPublicacionUsuario = "INSERT INTO publicacion (id,correo_usuario,texto,foto,link,estado,fecha,borrada) " \
                          "VALUES ({},'{}','{}','{}','{}','{}',TO_DATE('{}', 'DD/MM/YYYY'),{})"

INFO_PUBLICACION = "select id, texto, foto, link, estado, fecha from publicacion "\
                "where correo_usuario = '{}'"

def MenuVerPublicacion(usuario, conn):
    while True:
        ImprimirTitulo("ver publicaciones")
        Imprimir("Que desea hacer?\n"
                 "\t(1) Crear Publicacion\n"
                 "\t(2) Mis Publicaciones\n"
                 "\t(3) Otras Publicaciones\n"
                 "\t(4) Volver al menu anterior\n"
                 "\t(5) Salir\n")
        opcion = ValidarOpcion(range(1, 6))
        if opcion == 5:
            if HayConexionBD(conn):
                conn.close()
            sys.exit(0)
        elif opcion == 4:
            return
        elif opcion == 1:
            CrearPublicacionesUsuario(usuario, conn)
        elif opcion == 2:
            MisPublicaciones(usuario, conn)
        elif opcion == 3:
            Imprimir("Aqui van Otras Publicaciones")
            OtrasPublicaciones(usuario, conn)

def CrearPublicacionesUsuario(usuario, conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM publicacion ORDER BY id DESC LIMIT 1")
    id = cur.fetchall()
    id = id[0][0] + 1
    texto = PedirDescripcion("texto") #1000 chars
    foto = PedirDescripcion("foto") #30 chars
    link = PedirDescripcion("link") #100 chars
    opciones = ["Privada", "Publica"]
    ImprimirOpciones(opciones)
    seleccion = ValidarOpcion([1,2])
    if seleccion == 1:
        estado = "privada"
    else:
        estado = "publica"
    fechaCreacion = "{:%d-%m-%Y}".format(datetime.date.today())
    borrada = False
    opciones = ["Si", "No"]
    ImprimirOpciones(opciones, "Desea publicar?")
    seleccion = ValidarOpcion([1,2])
    if seleccion == 1:
        cur.execute(crearPublicacionUsuario.format(id,usuario,texto.strip("\n"),foto.strip("\n"),link.strip("\n"),estado,fechaCreacion,borrada))
        Imprimir("Publicacion creada")
        conn.commit()
    cur.close()
    return

def MisPublicaciones(usuario, conn):
    cur = conn.cursor()
    cur.execute(INFO_PUBLICACION.format(usuario))
    respuesta = cur.fetchall()
    tab = [["PUBLICACION", "TEXTO", "FOTO", "LINK", "ESTADO", "FECHA"]]
    opciones = []
    for i in respuesta:
        opciones.append(i[0])
        tab.append([i[0], i[1], i[2], i[3], i[4], i[5]])
    Imprimir(tabulate(tab))
    ops = ["Volver", "Salir"]
    ImprimirOpciones(ops, "", opciones[-1]+1)
    opciones.append(opciones[-1]+1)
    opciones.append(opciones[-1]+1)
    seleccion = ValidarOpcion(opciones)
    if seleccion == opciones[-1]:
        cur.close()
        conn.close()
        sys.exit()
    elif seleccion == opciones[-2]:
        return
    else:
        id_pub = seleccion
        ImprimirComentarios(id_pub, conn)
        opciones = ["Comentar",
                    "Eliminar Comentario",
                    "Editar Publicacion",
                    "Eliminar Publicacion",
                    "Volver",
                    "Salir"]
        ImprimirOpciones(opciones)
        seleccion = ValidarOpcion(range(1,len(opciones)+1))
        if seleccion == 1:
            Comentar(id_pub, conn)

        elif seleccion == 2:
            EliminarComentario(id_pub, conn)

        elif seleccion == 3:
            EditarPublicacion(id_pub, conn)

        elif seleccion == 4:
            EliminarPublicacion(id_pub, conn)

        elif seleccion == 5:
            return

        elif seleccion == 6:
            cur.close()
            conn.close()
            sys.exit()

def Comentar(id_a_comentar, conn, opcion): # opcion puede ser "comentario" o "publicacion"
    pass

def EliminarComentario(id_publicacion, conn):
    pass

def EditarPublicacion(id_publicacion, conn):
    pass

def EliminarPublicacion(id_publicacion, conn):
    pass

CONTACTOS_USUARIO = 'SELECT todos.amigo amigo' \
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
                    'ORDER BY todos.correo DESC'

EMPRESAS_POSTULADAS = "select distinct t.id_empresa " \
                      "from postulacion p, trabajo t " \
                      "where p.id_trabajo = t.id " \
                      "and p.correo_usuario = '{}'"

EMPRESAS_TRABAJADAS = "select distinct t.id_empresa from trabajado td, perfil pf, trabajo t " \
                        "where pf.correo_usuario = '{}' " \
                        "and td.id_perfil = pf.id " \
                        "and t.id = td.id_trabajo"

PUBLICACIONES_EMPRESAS = "select * from publicacion where id_empresa = {}"
PUBLICACIONES_AMIGOS = "select * from publicacion where correo_usuario = '{}'"
INFO_PUBLICACION_ID = "select p.texto, p.foto, p.link, p.estado, p.fecha, c.contenido " \
                      "from publicacion p, comentario c where c.id_publicacion = p.id " \
                        "and p.id = {}"


u = "Mono1Apellido1@gmail.com"

def OtrasPublicaciones(usuario, conn):
    ImprimirTitulo("otras publicaciones")
    cur = conn.cursor()
    cur.execute(CONTACTOS_USUARIO.format(usuario))
    amigos = cur.fetchall()
    lista_amigos = []
    for am in amigos:
        lista_amigos.append(am[0])
    ids_empresas = []
    cur.execute(EMPRESAS_POSTULADAS.format(usuario))
    empresas_postuladas = cur.fetchall()
    for ep in empresas_postuladas:
        ids_empresas.append(ep[0])
    cur.execute(EMPRESAS_TRABAJADAS.format(usuario))
    empresas_trabajadas = []
    for et in empresas_trabajadas:
        if et[0] not in ids_empresas:
            ids_empresas.append(et[0])

    atributos_publicacion_empresa = [["PUBLICACION", "REALIZADA",  "POR"], ["        ", "Empresa", "Amigo"]]
    ids_publicaciones = []
    for id in ids_empresas:
        cur.execute(PUBLICACIONES_EMPRESAS.format(id))
        res = cur.fetchall()
        for r in res:
            ids_publicaciones.append(r[0])
            atributos_publicacion_empresa.append([r[0], r[2], ""])
    for amigo in lista_amigos:
        cur.execute(PUBLICACIONES_AMIGOS.format(amigo))
        res = cur.fetchall()
        for r in res:
            ids_publicaciones.append(r[0])
            atributos_publicacion_empresa.append([r[0], "", r[1]])
    Imprimir(tabulate(atributos_publicacion_empresa))
    id_elegido = ValidarOpcion(ids_publicaciones, "Ingrese la publicacion que quiera ver en detalle: ")
    cur.execute(INFO_PUBLICACION_ID.format(id_elegido))
    info = cur.fetchall()
    info_publicacion = [["TEXTO", "FOTO", "LINK", "ESTADO", "FECHA", "COMENTARIOS"]]
    contador = 0
    for i in info:
        if contador == 0:
            info_publicacion.append([i[0], i[1], i[2], i[3], i[4], i[5]])
            contador += 1
        else:
            info_publicacion.append(["", "", "", "", "", i[5]])
    Imprimir(tabulate(info_publicacion))
    Imprimir("Que desea hacer?\n"
             "\t(1) Comentar\n"
             "\t(2) Eliminar comentario\n"
             "\t(3) Volver al menu anterior\n"
             "\t(4) Salir\n")
    opcion = ValidarOpcion(range(1, 5))
    if opcion == 4:
        if HayConexionBD(conn):
            conn.close()
        sys.exit(0)
    elif opcion == 3:
        return
    elif opcion == 1:
        print("comentar")
        Imprimir("Que desea comentar?\n"
                 "\t(1) Un comentario\n"
                 "\t(2) La publicacion\n")
        op_comentar = ValidarOpcion(range(1,3))
        if op_comentar == 1:
            pass
            #Comentar()
    elif opcion == 2:
        print("eliminar comentario")

OtrasPublicaciones(u, conn)


