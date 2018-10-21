from IO import *
from tabulate import *
#----QUERYS------
NombresEmpresas = "SELECT e.nombre, e.id " \
                  "FROM administrador a, empresa e " \
                  "WHERE a.id_empresa = e.id " \
                  "AND a.correo_usuario = '{}';"

IdTrabajo = "SELECT id " \
            "FROM trabajo " \
            "WHERE id_empresa = {}"

NombreApellidoFechaEstadoCorreoIDPostulacionPostulante = "SELECT pe.nombre, pe.apellido, po.fecha, po.estado, pe.correo_usuario, po.id " \
                           "FROM perfil pe, postulacion po " \
                           "WHERE pe.correo_usuario = po.correo_usuario " \
                           "AND po.id_trabajo = {}"

obtenerPerfil = "SELECT * " \
                "FROM perfil " \
                "WHERE correo_usuario = '{}'"

# Recibe el correo_usuario en usuario
def MenuEmpresas(usuario, conn):
    ImprimirTitulo("EMPRESAS")
    #seleccionar ver mis empresas o ver otros trabajos
    opciones = "(1) Empresas que soy administrador.\n" \
               "(2) Ver trabajos.[nada todavia]\n" \
               "(3) Salir\n"
    Imprimir(opciones)
    seleccion = ValidarOpcion(range(1,4))
    if seleccion == 3:
        sys.exit(0)
    elif seleccion == 1:
        MostrarMisEmpresas(usuario, conn)
    elif seleccion == 2:
        VerTrabajos2(conn)
    return


def MostrarMisEmpresas(usuario, conn):
    ImprimirTitulo("Mis Empresas")
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
                      "(2) Crear publicaciones. [nada todavia]\n" \
                      "(3) Mis publicaciones. [nada todavia]\n" \
                      "(4) Agregar administrador. [nada todavia]\n" \
                      "(5) Dejar de ser administrador. [nada todavia]\n" \
                      "(6) Crear empresas. [nada todavia]\n" \
                      "(7) Eliminar empresas. [nada todavia]\n" \
                      "(8) Volver.\n" \
                      "(9) Salir."
    Imprimir(opcionesEmpresa)
    seleccion = ValidarOpcion(range(1,10))
    if seleccion == 9:
        sys.exit(0)
    elif seleccion == 1:
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
    elif seleccion == 8:
        MenuEmpresas(usuario, conn)
    return


def VerTrabajos1(idEmpresa, conn):
    cur = conn.cursor()
    cur.execute("SELECT nombre FROM empresa WHERE id = {}".format(idEmpresa))
    nombreEmpresa = cur.fetchall()
    ImprimirTitulo("Trabajos en {}".format(nombreEmpresa[0][0]))
    cur.execute(IdTrabajo.format(idEmpresa))
    trabajos = cur.fetchall()
    i = 1
    for trabajo in trabajos:
        Imprimir("({}) Trabajo {}.".format(i, trabajo[0]))
        i += 1
    seleccion = ValidarOpcion(range(1, len(trabajos) + 1), "Seleccione un trabajo: ")
    VerTrabajo1(trabajos[seleccion-1], conn)
    return


# muestra las postulaciones de los usuarios junto con la fecha y estado de postulación
def VerTrabajo1(idTrabajo, conn):
    cur = conn.cursor()
    cur.execute("SELECT id_trabajo FROM trabajo WHERE id = {}".format(idTrabajo))
    idEmpresa = cur.fetchall()
    idEmpresa = idEmpresa[0][0]
    ImprimirTitulo("Postulantes")
    Imprimir("Id trabajo seleccionado: {}".format(idTrabajo[0]))
    cur.execute(NombreApellidoFechaEstadoCorreoIDPostulacionPostulante.format(idTrabajo[0]))
    postulantes = cur.fetchall()
    resultadoPostulantes = [['Nombre','Apellido','Fecha postulacion', 'Estado']]
    for postulante in postulantes:
        resultadoPostulantes.append([postulante[0],postulante[1],postulante[2],postulante[3]])
    Imprimir(tabulate(resultadoPostulantes,headers='firstrow',showindex=range(1,len(postulantes)+1)))
    postulanteSeleccionado = ValidarOpcion(range(1,len(postulantes)+1),"Seleccionar postulante: ")
    correoPostulanteSeleccionado =  postulantes[postulanteSeleccionado-1][4]
    idPostulacion = postulantes[postulanteSeleccionado-1][5]
    opciones = "(1) Ver perfil postulante.\n" \
               "(2) Aceptar postulacion.\n" \
               "(3) Rechazar postulacion.\n" \
               "(4) Volver.\n" \
               "(5) Salir."
    Imprimir(opciones)
    seleccion = ValidarOpcion(range(1,4))
    if seleccion == 1:
        VerPerfilPostulante(correoPostulanteSeleccionado, conn)
    elif seleccion == 2:
        AceptarPostulacion(idPostulacion, conn)
    elif seleccion == 3:
        RechazarPostulacion(idPostulacion, conn)
    elif seleccion == 4:
        VerTrabajos1(idEmpresa, conn)
    elif seleccion == 5:
        sys.exit()
    return

#selecciona una postulación y se muestra el perfil del postulante
def VerPerfilPostulante(correoPostulante, conn):
    ImprimirTitulo("Perfil de {}".format(correoPostulante))
    cur = conn.cursor()
    cur.execute(obtenerPerfil.format(correoPostulante))
    datosPerfil = cur.fetchall()
    datos = [["Id","Correo","Nombre","Apellido","Fecha nacimiento","Pais","Sexo","Descripcion"]]
    for dato in datosPerfil:
        datos.append(dato)
    Imprimir(tabulate(datos,headers='firstrow'))
    return


# cambia el estado de la postulación a aceptado, mandando una notificación al usuario
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