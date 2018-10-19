from IO import *
import tabulate
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

# Recibe el correo_usuario en usuario
def MenuEmpresas(usuario, conn):
    Imprimir("\nEmpresas.")
    #seleccionar ver mis empresas o ver otros trabajos
    opciones = "(1) Empresas que soy administrador.\n" \
               "(2) Ver trabajos.[nada todavia]"
    Imprimir(opciones)
    seleccion = ValidarOpcion(range(1,3))
    if seleccion == 1:
        MostrarMisEmpresas(usuario, conn)
    elif seleccion == 2:
        VerTrabajos2(conn)
    return


def MostrarMisEmpresas(usuario, conn):
    Imprimir("\nMis Empresas")
    cur = conn.cursor()
    cur.execute(NombresEmpresas.format(usuario))
    empresas = cur.fetchall()
    i = 1
    for empresa in empresas:
        Imprimir("({}): {}".format(i,empresa[0]))
        i += 1
    seleccion = ValidarOpcion(range(1, len(empresas) + 1), "Seleccione una empresa: ")
    idEmpresaSeleccionada = empresas[seleccion-1][1]
    Imprimir("Empresa seleccionada: {}".format(empresas[seleccion-1][0]))
    opcionesEmpresa = "(1) Ver trabajos.\n" \
                      "(2) Crear publicaciones.[nada todavia]\n" \
                      "(3) Mis publicaciones.[nada todavia]\n" \
                      "(4) Agregar administrador.[nada todavia]\n" \
                      "(5) Dejar de ser administrador.[nada todavia]\n" \
                      "(6) Crear empresas.[nada todavia]\n" \
                      "(7) Eliminar empresas.[nada todavia]"
    Imprimir(opcionesEmpresa)
    seleccion = ValidarOpcion(range(1,8))
    if seleccion == 1:
        VerTrabajos1(idEmpresaSeleccionada, conn)
    elif seleccion == 2:
        CrearPublicaciones(conn)
    elif seleccion == 3:
        MisPublicaciones(usuario, conn)
    elif seleccion == 4:
        AgregarAdministrador(idEmpresaSeleccionada, conn)
    elif seleccion == 5:
        DejarDeSerAdministrador(usuario, conn)
    elif seleccion == 6:
        CrearEmpresa(conn)
    elif seleccion == 7:
        EliminarEmpresa(idEmpresaSeleccionada, conn)
    return


def VerTrabajos1(idEmpresa, conn):
    Imprimir("Trabajos de la empresa {}".format(idEmpresa))
    cur = conn.cursor()
    cur.execute(IdTrabajo.format(idEmpresa))
    trabajos = cur.fetchall()
    for trabajo in trabajos:
        Imprimir("({}) Trabajo {}.".format(trabajo[0]))
    seleccion = ValidarOpcion(range(1, len(trabajos) + 1), "Seleccione un trabajo: ")
    VerTrabajo1(trabajos[seleccion-1], conn)
    return

# muestra las postulaciones de los usuarios junto con la fecha y estado de postulación
def VerTrabajo1(idTrabajo, conn):
    Imprimir("\nId trabajo seleccionado: {}".format(idTrabajo[0]))
    cur = conn.cursor()
    cur.execute(NombreApellidoPostulante.format(idTrabajo[0]))
    postulantes = cur.fetchall()

    return


def VerPerfilPostulante(correoPostulante, conn):
    return


def AceptarPostulacion(idPostulacion, conn):
    return


def RechazarPostulacion(idPostulacion, conn):
    return

def CerrarPostulaciones(idTrabajo, conn):
    return

def AgregarTrabajos(conn):
    return

def EliminarTrabajo(idTrabajo, conn):
    return

def CrearPublicaciones(conn):
    return

def MisPublicaciones(correoUsuario, conn):
    return

def VerPublicacion(idPublicacion, conn):
    return

def EliminarPublicacion(idPublicacion, conn):
    return

def Comentar(idPublicacion, conn, idComentado = None):
    return

def AgregarAdministrador(idEmpresa, conn):
    return

def DejarDeSerAdministrador(correoUsuario, conn):
    return

def CrearEmpresa(conn):
    return

def EliminarEmpresa(idEmpresa, conn):
    return

def VerTrabajos2(conn):
    return

def VerEmpresa(idEmpresa, conn):
    return

def VerTrabajo2(idTrabajo, conn):
    return

def PostularTrabajo(idTrabajo, correoUsuario, conn):
    return