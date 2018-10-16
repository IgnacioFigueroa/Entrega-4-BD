# -*- coding: utf-8 -*-
import psycopg2
from IniciarSesion import *
from CrearCuenta import *
from RecuperarContraseña import *

def Imprimir(mensaje):
    print(mensaje)


def ImprimirError(mensaje):
    print(mensaje)


def ImprimirPositivo(mensaje):
    print(mensaje)


conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")



# Menu
if __name__ == '__main__':
    Imprimir("BIENVENIDO/A A LINKEDING")
    Imprimir("Que desea hacer?\n"
             "\t(1) Iniciar Sesion\n"
             "\t(2) Crear Cuenta\n"
             "\t(3) Recuperar Contraseña\n")
    opcion = int(input("Ingrese su opcion"))
    while opcion not in range(1, 4):
        ImprimirError("Ingrese una opcion valida")
        opcion = input("Ingrese su opcion")

    if opcion == 1:
        IniciarSesion()
    elif opcion == 2:
        CrearCuenta()
    elif opcion == 3:
        RecuperarContrasena()


