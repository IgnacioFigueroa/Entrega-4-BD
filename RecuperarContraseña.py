from datetime import date
from IO import *

def RecuperarContrasena(conn):
        cur = conn.cursor()
        cur.execute("select * from contrasena_antigua")
        ca = cur.fetchall()
        dicCorreoContra = {}
        dicCorreoId = {}
        for tupla in ca:
            dicCorreoContra[tupla[1]] = tupla[2]
            dicCorreoId[tupla[1]] = tupla[0]

        correo = input("Ingrese su correo electronico: ")
        while correo not in dicCorreoContra.keys():
            correo = input("Correo no valido, ingreselo nuevamente: ")
        Imprimir("Su contrasena actual es: " + dicCorreoContra[correo])
        contraNueva = input("Ingrese una contrasena nueva: ")
        while len(contraNueva) not in range(1, 31):
            contraNueva = input("Largo de la contrasena invalido, ingrese una contrasena nueva: ")

        idNuevo = max(dicCorreoId.values()) + 1
        fechaActual = date.today()

        #print("Insertando en contrasena_antigua:\nid:",
        #      idNuevo, "\ncorreo:", correo, "\ncontrasena nueva:",
        #      contraNueva, "\nfecha actual:", fechaActual)

        cur.execute("insert into contrasena_antigua(id, correo_usuario, contrasena, fecha_creacion) "
                    "values({},'{}','{}','{}');".format(idNuevo, correo, contraNueva, fechaActual))
        conn.commit()
        cur.close()