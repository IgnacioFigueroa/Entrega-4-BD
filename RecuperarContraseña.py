import time
from IO import *
def RecuperarContrasena(conn):
        cur = conn.cursor()
        cur.execute("select * from contrasena_antigua")
        ca = cur.fetchall()
        dic_correo_contra = {}
        dic_correo_id = {}
        for tupla in ca:
            dic_correo_contra[tupla[1]] = tupla[2]
            dic_correo_id[tupla[1]] = tupla[0]

        correo = input("Ingrese su correo electronico: ")
        while correo not in dic_correo_contra.keys():
            correo = input("Correo no valido, ingreselo nuevamente: ")
        Imprimir("Su contrasena actual es:" + dic_correo_contra[correo])
        contra_nueva = input("Ingrese una contrasena nueva: ")
        while len(contra_nueva) not in range(1, 31):
            contra_nueva = input("Largo de la contrasena invalido, ingrese una contrasena nueva: ")
