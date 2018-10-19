import time
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
        Imprimir("Su contrasena actual es:" + dicCorreoContra[correo])
        contraNueva = input("Ingrese una contrasena nueva: ")
        while len(contraNueva) not in range(1, 31):
            contraNueva = input("Largo de la contrasena invalido, ingrese una contrasena nueva: ")
