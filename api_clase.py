# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:51:18 2018

@author: sjfig
"""

import psycopg2
import IniciarSesion

def imprimir(mensaje):
    print(mensaje)


conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")

cur = conn.cursor()

# Menu
imprimir("BIENVENIDO/A A LINKEDING")
imprimir()