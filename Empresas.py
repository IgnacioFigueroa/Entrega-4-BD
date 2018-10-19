from IO import *
#----QUERYS------
NombresEmpresas = "SELECT e.nombre, e.id " \
                  "FROM administrador a, empresa e " \
                  "WHERE a.id_empresa = e.id " \
                  "AND a.correo_usuario = '{}';"

IdTrabajo = "SELECT id " \
            "FROM trabajo " \
            "WHERE id_empresa = {}"

NombreApellidoPostulante = "SELECT pe.nombre, pe.apellido " \
                           "FROM perfil pe, postulacion po " \
                           "WHERE pe.correo_usuario = po.correo_usuario " \
                           "AND po.id_trabajo = {}"


def MenuEmpresas(usuario, conn):
    Imprimir("\nMis Empresas")
    Imprimir("Seleccione una empresa, ingrese 0 para salir.")
    Empresas = MostrarMisEmpresas(usuario, conn)
    seleccion = ValidarOpcion(range(0,len(Empresas)+1))
    if (seleccion == "0"):
        return 0
    idEmpresaSeleccionada = Empresas[seleccion-1][1]
    Imprimir("Trabajos de la empresa {}".format(idEmpresaSeleccionada))
    Trabajos = VerTrabajos(idEmpresaSeleccionada,conn)
    seleccion = ValidarOpcion(range(1,len(Trabajos)+1))
    return


def MostrarMisEmpresas(usuario, conn):
    cur = conn.cursor()
    cur.execute(NombresEmpresas.format(usuario))
    empresas = cur.fetchall()
    i = 1
    for empresa in empresas:
        Imprimir("({}): {}".format(i,empresa[0]))
        i += 1
    return empresas

def VerTrabajos(idEmpresa, conn):
    cur = conn.cursor()
    cur.execute(IdTrabajo.format(idEmpresa))
    trabajos = cur.fetchall()
    i = 1
    for trabajo in trabajos:
        cur.execute(NombreApellidoPostulante.format(trabajo[0]))
        postulantes = cur.fetchall()
        Imprimir("({}) Trabajo {}. Postulaciones: {}".format(i,trabajo[0],len(postulantes)))
        Imprimir("\tPostulantes:")
        for postulante in postulantes:
            Imprimir("\t\t{} {}".format(postulante[0],postulante[1]))
        Imprimir("")
        i += 1
    return trabajos
