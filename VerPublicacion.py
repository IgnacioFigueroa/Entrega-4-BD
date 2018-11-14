from IO import *
import datetime

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
    return

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
            pass

        elif seleccion == 3:
            pass

        elif seleccion == 4:
            pass

        elif seleccion == 5:
            return

        elif seleccion == 6:
            cur.close()
            conn.close()
            sys.exit()

def Comentar(id_publicacion, conn):
    pass



def OtrasPublicaciones(conn):
    pass
