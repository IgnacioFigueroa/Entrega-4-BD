# -*- coding: utf-8 -*-
import psycopg2
from CrearCuenta import CrearCuenta
from IO import *
from MenuPrincipal import MenuPrincipal
from RecuperarContraseña import RecuperarContrasena
from IniciarSesion import IniciarSesion
import sys
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")

# MENU
if __name__ == '__main__':
    ImprimirTitulo("BIENVENIDO/A A LINKEDING")
    Imprimir("Que desea hacer?\n"
             "\t(1) Iniciar Sesion\n"
             "\t(2) Crear Cuenta\n"
             "\t(3) Recuperar Contraseña\n"
             "\t(4) Salir\n")
    opcion = ValidarOpcion(range(1, 4))
    if opcion == 1:
        usuario = IniciarSesion(conn)
        MenuPrincipal(usuario, conn)
    elif opcion == 2:
        CrearCuenta(conn)
    elif opcion == 3:
        RecuperarContrasena(conn)
    elif opcion == 4:
        sys.exit(0)
    conn.close()

