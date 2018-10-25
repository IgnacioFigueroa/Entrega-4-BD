from IO import *
from tabulate import tabulate
import psycopg2
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")

u = "Mono35Apellido35@gmail.com"

def MenuVerNotificacion(usuario, conn):
    cur = conn.cursor()
    cur.execute("select * from notificacion where leida = FALSE"
                " and correo_usuario = '{}';".format(usuario))
    notis = cur.fetchall()
    ImprimirTitulo("NOTIFICACIONES NO LEIDAS")
    ListaNotificaciones = []
    ln = []
    for n in notis:
        ListaNotificaciones.append([n[0]])
        ln.append(n[0])

    hay_notis = False
    if len(ln) > 0:
        hay_notis = True
        Imprimir(tabulate(ListaNotificaciones))
        Imprimir("Que desea hacer?\n"
                 "\t(1) Ver notificacion\n"
                 "\t(2) Seleccionar todas las notificaciones como leidas\n"
                 "\t(3) Ver notificaciones leidas\n"
                 "\t(4) Volver al menu anterior\n"
                 "\t(5) Salir\n")
        opcion = ValidarOpcion(range(1, 6))
    else:
        Imprimir("No hay notificaciones no leidas\n")
        Imprimir("Que desea hacer?\n"
                 "\t(1) Ver notificaciones leidas\n"
                 "\t(2) Volver al menu anterior\n"
                 "\t(3) Salir\n")
        opcion = ValidarOpcion(range(1, 4))

    if (opcion == 5 and hay_notis) or (opcion == 3 and not hay_notis):
        sys.exit(0)
    elif (opcion == 4 and hay_notis) or (opcion == 2 and not hay_notis):
        return
    elif opcion == 1 and hay_notis:
        opcionNotificacion = ValidarOpcion(ln, "Seleccione la notificacion que quiere ver: ")
        for n in notis:
            if n[0] == opcionNotificacion:
                #n[0] = id, n[1] = id_comentario, n[2] = correo_usuario, n[3] = leida,
                #n[4] = id_validacion, n[5] = id_postulacion, n[6] = id_solicitud
                print(n)
                if n[1] != None:
                    print("es comentario")
                    cur.execute("select c.id, c.id_comentado, c.correo_usuario_comentador,"
                                " c.id_publicacion, c.contenido, c.fecha, c.borrado"
                                " from comentario c, notificacion n where {} = c.id;".format(n[1]))
                    info_comentario = cur.fetchone()
                    if info_comentario[1] == None: #no es comentario de otro comentario
                        pass
                        atributos_comentario = [""]
                    print(info_comentario)
                elif n[4] != None:
                    print("es validacion")
                elif n[5] != None:
                    print("es postulacion")
                elif n[6] != None:
                    print("es solicitud")
        """
        atributosNotificacion = ["Notificacion", "Evento", "Correo", "Leida"]
        ListaNotisDetalles = []
        for n in notis:
            if n[0] == opcionNotificacion:
                for i in range(len(atributosNotificacion)):
                   ListaNotisDetalles.append([atributosNotificacion[i], n[i]])
        Imprimir(tabulate(ListaNotisDetalles))
        """
        #cur.execute("update notificacion set leida = TRUE"
        #            " where id = {} and correo_usuario = '{}';".format(opcionNotificacion, usuario))
        #conn.commit()

    elif opcion == 2 and hay_notis:
        cur.execute("update notificacion set leida = TRUE"
                    " where leida = FALSE and correo_usuario = '{}';".format(usuario))
        conn.commit()
    elif (opcion == 3 and hay_notis) or (opcion == 1 and not hay_notis):
        ImprimirTitulo("NOTIFICACIONES LEIDAS")
        cur.execute("select * from notificacion where leida = TRUE"
                    " and correo_usuario = '{}';".format(usuario))
        notisLeidas = cur.fetchall()
        lnl = []
        ListaNotificacionesLeidas = []
        for nl in notisLeidas:
            ListaNotificacionesLeidas.append([nl[0]])
            lnl.append(nl[0])
        Imprimir(tabulate(ListaNotificacionesLeidas))
        respuesta = ValidarOpcion(range(1,3),"Quiere ver alguna notificacion en detalle?\n"
                          "\t(1) si\n"
                          "\t(2) no\n"
                          "Ingrese su opcion: ")
        if respuesta == 1:
            opcionNotificacionLeida = ValidarOpcion(lnl, "Seleccione la notificacion que quiere ver: ")
            atributosNotificacion = ["Notificacion", "Publicacion", "Correo", "Leida"]
            ListaNotisDetalles = []
            for n in notisLeidas:
                if n[0] == opcionNotificacionLeida:
                    for i in range(len(atributosNotificacion)):
                        ListaNotisDetalles.append([atributosNotificacion[i], n[i]])
            Imprimir(tabulate(ListaNotisDetalles))

    cur.close()
    conn.close()


MenuVerNotificacion(u, conn)