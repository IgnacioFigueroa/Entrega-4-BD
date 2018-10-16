# -*- coding: utf-8 -*-
import psycopg2
from CrearCuenta import crear_cuenta
from IO import *
from MenuPrincipal import menu_principal
from RecuperarContraseña import recuperar_contrasena
from IniciarSesion import iniciar_sesion
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")

# Menu
if __name__ == '__main__':
    imprimir("BIENVENIDO/A A LINKEDING")
    imprimir("Que desea hacer?\n"
             "\t(1) Iniciar Sesion\n"
             "\t(2) Crear Cuenta\n"
             "\t(3) Recuperar Contraseña\n")
    opcion = validar_opcion(range(1,4))
    if opcion == 1:
        usuario = iniciar_sesion(conn)
        menu_principal(usuario, conn)
    elif opcion == 2:
        crear_cuenta(conn)
    elif opcion == 3:
        recuperar_contrasena(conn)


