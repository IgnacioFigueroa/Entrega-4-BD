from IO import *


def MenuEmpresas(usuario, conn):
    Imprimir("\nMis Empresas")
    Imprimir("Seleccione una empresa, ingrese 0 para salir.")
    cantidadEmpresas = MostrarMisEmpresas(usuario, conn)
    seleccion = input("Ingrese su opcion: ")
    ValidarOpcion(range(0,cantidadEmpresas))
    return


def MostrarMisEmpresas(usuario, conn):
    cur = conn.cursor()
    empresas = cur.execute("SELECT e.nombre FROM administrador a, empresa e WHERE a.id_empresa = e.id AND a.correo_usuario = '{}';".format(usuario))
    empresas = cur.fetchall()
    i = 1
    for empresa in empresas:
        Imprimir("Nombre empresa: {}".format(empresa[0]))
    return len(empresas)

