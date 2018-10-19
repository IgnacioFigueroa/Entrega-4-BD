import psycopg2
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")
from IO import *
from tabulate import tabulate
u = "Mono49Apellido49@gmail.com"
def MenuVerNotificacion(usuario, conn):
    cur = conn.cursor()
    cur.execute("select * from notificacion_publicacion where leida = FALSE"
                " and correo_usuario = '{}';".format(usuario))
    notis = cur.fetchall()
    Imprimir("NOTIFICACIONES NO LEIDAS")
    ListaNotificaciones = []
    ln = [8]
    for n in notis:
        ListaNotificaciones.append([n[0]])
        ln.append(n[0])
    Imprimir(tabulate(ListaNotificaciones))
    print(ln)
    Imprimir("Que desea hacer?\n"
             "\t(1) Ver notificacion\n"
             "\t(2) Seleccionar todas las notificaciones como leidas\n"
             "\t(3) Ver notificaciones leidas\n")
    opcion = ValidarOpcion(range(1, 4))
    if opcion == 1:
        pass
        #opcionNotificacion = ValidarOpcion(ln)
        """"
        opcionNotificacion = input("Seleccione la notificacion que quiere ver: ")
        while int(opcionNotificacion) not in ln:
            opcionNotificacion = input("Seleccione una notificacion valida: ")
        print(opcionNotificacion)
        """
    elif opcion == 2:
        cur.execute("update notificacion_publicacion set leida = TRUE"
                    " where leida = FALSE and correo_usuario = '{}';".format(usuario))
        conn.commit()
    elif opcion == 3:
        cur.execute("select * from notificacion_publicacion where leida = TRUE"
                    " and correo_usuario = '{}';".format(usuario))
        notisLeidas = cur.fetchall()
        lnl = []
        ListaNotificacionesLeidas = []
        for nl in notisLeidas:
            ListaNotificacionesLeidas.append(nl[0])
            lnl.append(nl[0])


    cur.close()
    conn.close()

MenuVerNotificacion(u, conn)

print()
print("++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++")
print()