from IO import *
from tabulate import *
import datetime
#----QUERYS------
NombresEmpresas = "SELECT e.nombre, e.id " \
                  "FROM administrador a, empresa e " \
                  "WHERE a.id_empresa = e.id " \
                  "AND a.correo_usuario = '{}';"

IdTrabajo = "SELECT id " \
            "FROM trabajo " \
            "WHERE id_empresa = {} " \
            "ORDER BY id ASC"

NombreApellidoFechaEstadoCorreoIDPostulacionPostulante = "SELECT pe.nombre, pe.apellido, po.fecha, po.estado, pe.correo_usuario, po.id " \
                           "FROM perfil pe, postulacion po " \
                           "WHERE pe.correo_usuario = po.correo_usuario " \
                           "AND po.id_trabajo = {}"

obtenerPerfil = "SELECT * " \
                "FROM perfil " \
                "WHERE correo_usuario = '{}'"

aceptarPostulacion = "UPDATE postulacion " \
                     "SET estado = 'Aceptado' " \
                     "WHERE id = {}"

rechazarPostulacion = "UPDATE postulacion " \
                     "SET estado = 'Rechazado' " \
                     "WHERE id = {}"

abrirPostulaciones = "UPDATE trabajo " \
                      "SET postulacion_abierta = 'True' " \
                      "WHERE id = {}"

cerrarPostulaciones = "UPDATE trabajo " \
                      "SET postulacion_abierta = 'False' " \
                      "WHERE id = {}"

agregarTrabajo = "INSERT INTO trabajo (id, id_empresa, descripcion, fecha_creacion, postulacion_abierta) " \
                 "VALUES ({}, {}, '{}', TO_DATE('{}', 'DD/MM/YYYY'), {})"

eliminarTrabajo = "DELETE FROM trabajo WHERE id = {}"

crearPublicacionEmpresa = "INSERT INTO publicacion (id,id_empresa,texto,foto,link,estado,fecha,borrada) " \
                          "VALUES ({},{},'{}','{}','{}','{}',TO_DATE('{}', 'DD/MM/YYYY'),{})"

verPublicacionesEmpresaCorto = "SELECT id, texto FROM publicacion WHERE id_empresa = {}"
verPublicacionesEmpresa = "SELECT * FROM publicacion WHERE id_empresa = {}"
verPublicacion = "SELECT * FROM publicacion WHERE id = {}"

eliminarPublicacion = "DELETE FROM publicacion WHERE id = {};"

comentar = "INSERT INTO comentario (id, id_comentado, correo_usuario_comentador, id_publicacion, contenido, fecha, borrado) " \
           "VALUES ({},{},'{}',{},'{}',TO_DATE('{}', 'DD/MM/YYYY'),{})"

# Recibe el correo_usuario en usuario
def MenuEmpresas(usuario, conn):
    ImprimirTitulo("EMPRESAS")
    #seleccionar ver mis empresas o ver otros trabajos
    opciones = ["Empresas que soy administrador",
               "Ver trabajos [nada todavia]",
               "Salir"]
    ImprimirOpciones(opciones)
    seleccion = ValidarOpcion(range(1,len(opciones)+1))
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
    opcionesEmpresa = ["Ver trabajos",
                      "Crear publicaciones",
                      "Mis publicaciones",
                      "Agregar administrador [nada todavia]",
                      "Dejar de ser administrador [nada todavia]",
                      "Crear empresas [nada todavia]",
                      "Eliminar empresas [nada todavia]",
                      "Volver",
                      "Salir"]
    ImprimirOpciones(opcionesEmpresa)
    cur.close()
    seleccion = ValidarOpcion(range(1,len(opcionesEmpresa)+1))
    if seleccion == 9:
        sys.exit(0)
    elif seleccion == 1:
        VerTrabajos1(idEmpresaSeleccionada, conn)
        MostrarMisEmpresas(usuario, conn)
    elif seleccion == 2:
        CrearPublicaciones(idEmpresaSeleccionada, conn)
        MostrarMisEmpresas(usuario, conn)
    elif seleccion == 3:
        MisPublicaciones(idEmpresaSeleccionada, conn)
        MostrarMisEmpresas(usuario, conn)
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
    opciones = "({}) Volver.\n" \
               "({}) Salir.".format(i, i+1)
    Imprimir(opciones)
    seleccion = ValidarOpcion(range(1, i+2), "Seleccione un trabajo: ")
    cur.close()
    if seleccion == i:
        return
    elif seleccion == i+1:
        sys.exit()
    else:
        idTrabajo = trabajos[seleccion-1]
        opciones = ["Ver trabajo","Abrir postulaciones", "Cerrar postulaciones", "Agregar trabajos", "Eliminar trabajo", "Volver", "Salir"]
        ImprimirOpciones(opciones)
        seleccion = ValidarOpcion(range(1,len(opciones)+1))
        if seleccion == 1:
            VerTrabajo1(idTrabajo, conn)
        elif seleccion == 2:
            AbrirPostulaciones(idTrabajo, conn)
        elif seleccion == 3:
            CerrarPostulaciones(idTrabajo, conn)
        elif seleccion == 4:
            AgregarTrabajos(idEmpresa, conn)
        elif seleccion == 5:
            EliminarTrabajo(idTrabajo, conn)
        elif seleccion == 6:
            return
        elif seleccion == 7:
            sys.exit()
        VerTrabajos1(idEmpresa, conn)
    return


# muestra las postulaciones de los usuarios junto con la fecha y estado de postulación
def VerTrabajo1(idTrabajo, conn):
    cur = conn.cursor()
    cur.execute("SELECT id_empresa FROM trabajo WHERE id = {}".format(idTrabajo[0]))
    idEmpresa = cur.fetchall()
    idEmpresa = idEmpresa[0][0]
    ImprimirTitulo("Postulantes")
    Imprimir("Id trabajo seleccionado: {}".format(idTrabajo[0]))
    cur.execute("SELECT postulacion_abierta FROM trabajo WHERE id = {}".format(idTrabajo[0]))
    estadoPostulaciones = cur.fetchall()
    estadoPostulaciones = estadoPostulaciones[0][0]
    if estadoPostulaciones == True:
        estadoPostulaciones = "abiertas"
    else:
        estadoPostulaciones = "cerradas"
    Imprimir("Postulaciones {}\n".format(estadoPostulaciones))

    cur.execute(NombreApellidoFechaEstadoCorreoIDPostulacionPostulante.format(idTrabajo[0]))
    postulantes = cur.fetchall()
    resultadoPostulantes = [['Nombre','Apellido','Fecha postulacion', 'Estado']]
    for postulante in postulantes:
        resultadoPostulantes.append([postulante[0],postulante[1],postulante[2],postulante[3]])
    if len(resultadoPostulantes)>1:
        Imprimir(tabulate(resultadoPostulantes,headers='firstrow',showindex=range(1,len(postulantes)+1)))
        postulanteSeleccionado = ValidarOpcion(range(1,len(postulantes)+1),"Seleccionar postulante: ")
        correoPostulanteSeleccionado = postulantes[postulanteSeleccionado - 1][4]
        idPostulacion = postulantes[postulanteSeleccionado-1][5]
        opciones = "(1) Ver perfil postulante.\n" \
                   "(2) Aceptar postulacion.\n" \
                   "(3) Rechazar postulacion.\n" \
                   "(4) Volver.\n" \
                   "(5) Salir."
        Imprimir(opciones)
        seleccion = ValidarOpcion(range(1, 6))
        cur.close()
        if seleccion == 1:
            VerPerfilPostulante(correoPostulanteSeleccionado, conn)
            VerTrabajo1(idTrabajo, conn)
        elif seleccion == 2:
            AceptarPostulacion(idPostulacion, conn)
            VerTrabajo1(idTrabajo, conn)
        elif seleccion == 3:
            RechazarPostulacion(idPostulacion, conn)
            VerTrabajo1(idTrabajo, conn)
        elif seleccion == 4:
            VerTrabajos1(idEmpresa, conn)
        elif seleccion == 5:
            sys.exit()
    else:
        Imprimir("No hay postulantes ); ...pero ya vendran :)")
        ImprimirOpciones(["Volver", "Salir"])
        seleccion = ValidarOpcion(range(1,3))
        if seleccion == 1:
            VerTrabajos1(idEmpresa, conn)
        elif seleccion == 2:
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
    opciones = "\n(0) Volver.\n" \
               "(1) Salir."
    Imprimir(opciones)
    seleccion = ValidarOpcion(range(0,2))
    cur.close()
    if seleccion == 0:
        return
    elif seleccion == 1:
        sys.exit()
    return


# cambia el estado de la postulación a aceptado, mandando una notificación al usuario
def AceptarPostulacion(idPostulacion, conn):
    cur = conn.cursor()
    cur.execute(aceptarPostulacion.format(idPostulacion))#cambia el estado de la postulacion
    ImprimirPositivo("Postulacion aceptada.")
    conn.commit()
    cur.close()
    return


def RechazarPostulacion(idPostulacion, conn):
    cur = conn.cursor()
    cur.execute(rechazarPostulacion.format(idPostulacion))#cambia el estado de la postulacion
    ImprimirPositivo("Postulacion rechazada.")
    conn.commit()
    cur.close()
    return


def AbrirPostulaciones(idTrabajo, conn):
    cur = conn.cursor()
    cur.execute(abrirPostulaciones.format(idTrabajo[0]))
    Imprimir("Postulaciones abiertas.")
    conn.commit()
    cur.close()
    return


def CerrarPostulaciones(idTrabajo, conn):
    cur = conn.cursor()
    cur.execute(cerrarPostulaciones.format(idTrabajo[0]))
    Imprimir("Postulaciones cerradas.")
    conn.commit()
    cur.close()
    return


def AgregarTrabajos(idEmpresa, conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM trabajo ORDER BY id DESC LIMIT 1")
    idNuevoTrabajo = cur.fetchall()
    idNuevoTrabajo = idNuevoTrabajo[0][0] + 1
    descripcion = PedirDescripcion()
    fechaCreacion = "{:%d-%m-%Y}".format(datetime.date.today())
    postulacionAbierta = ValidarOpcion([1,2],"(1) Postulaciones abiertas.\n(2) Postulaciones cerradas.")
    if postulacionAbierta == 1:
        postulacionAbierta = "TRUE"
    else:
        postulacionAbierta = "FALSE"
    cur.execute(agregarTrabajo.format(idNuevoTrabajo, idEmpresa, descripcion, fechaCreacion, postulacionAbierta))
    Imprimir("Trabajo agregado.")
    conn.commit()
    cur.close()
    return


def EliminarTrabajo(idTrabajo, conn):
    cur = conn.cursor()
    ImprimirOpciones(["Si", "No"], "Esta seguro que desea eliminar este trabajo?")
    seleccion = ValidarOpcion([1,2])
    if seleccion == 1:
        cur.execute(eliminarTrabajo.format(idTrabajo[0]))
        conn.commit()
    else:
        Imprimir("No se eliminara.")
    cur.close()
    return


def CrearPublicaciones(idEmpresa, conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM publicacion ORDER BY id DESC LIMIT 1")
    id = cur.fetchall()
    id = id[0][0] + 1
    texto = PedirDescripcion("texto") #1000 chars
    foto = PedirDescripcion("foto") #30 chars
    link = PedirDescripcion("link") #100 chars
    opciones = ["Privada", "Publica"]
    ImprimirOpciones(opciones)
    seleccion = ValidarOpcion([1,2])
    if seleccion == 1:
        estado = "privada"
    else:
        estado = "publica"
    fechaCreacion = "{:%d-%m-%Y}".format(datetime.date.today())
    borrada = False
    opciones = ["Si", "No"]
    ImprimirOpciones(opciones, "Desea publicar?")
    seleccion = ValidarOpcion([1,2])
    if seleccion == 1:
        cur.execute(crearPublicacionEmpresa.format(id,idEmpresa,texto,foto,link,estado,fechaCreacion,borrada))
        Imprimir("Publicacion creada.")
        conn.commit()
    cur.close()
    return


# Mostrar una lista con todas las publicaciones que a creado la empresa con las siguientes opciones.
# Una vez que el usuario seleccione debe mostrar el contenido de la publicacion, el tipo de publicacion
# y una lista de los comentarios que tiene la publicacion.
def MisPublicaciones(idEmpresa, conn):
    cur = conn.cursor()
    cur.execute(verPublicacionesEmpresaCorto.format(idEmpresa))
    publicacionesCorto = cur.fetchall()
    publicacionesCorto.append(["Volver",""])
    publicacionesCorto.append(["Salir",""])
    Imprimir(tabulate(publicacionesCorto,headers=["Id", "Texto"],showindex=range(1,len(publicacionesCorto)+1)))
    seleccion = ValidarOpcion(range(1,len(publicacionesCorto)+1),"Seleccione una publicacion: ")
    idPublicacionSeleccionada = publicacionesCorto[seleccion-1][0]
    if idPublicacionSeleccionada == "Volver":
        cur.close()
        return
    elif idPublicacionSeleccionada == "Salir":
        cur.close()
        sys.exit()

    ImprimirTitulo("Publicacion #{}".format(idPublicacionSeleccionada))
    cur.execute(verPublicacion.format(idPublicacionSeleccionada))
    contenidoPublicacion = cur.fetchall()
    ImprimirInfoPublicacion(contenidoPublicacion)
    ImprimirComentarios(idPublicacionSeleccionada, conn)

    opciones = ["Ver publicacion",
                "Eliminar publicacion",
                "Comentar",
                "Volver",
                "Salir"]
    ImprimirOpciones(opciones)
    seleccion = ValidarOpcion(range(1, len(opciones)+1))
    if seleccion == 1:
        VerPublicacion(idPublicacionSeleccionada, conn)
        MisPublicaciones(idEmpresa, conn)
    elif seleccion == 2:
        EliminarPublicacion(idPublicacionSeleccionada, conn)
    elif seleccion == 3:
        cur.execute("SELECT nombre FROM empresa WHERE id = {}".format(idEmpresa))
        nombreEmpresa = cur.fetchall()
        nombreEmpresa = nombreEmpresa[0][0]
        Comentar(idPublicacionSeleccionada, conn, nombreEmpresa)
    elif seleccion == 4:
        cur.close()
        MisPublicaciones(idEmpresa, conn)
    elif seleccion == 5:
        cur.close()
        sys.exit()
    cur.close()
    return


def VerPublicacion(idPublicacion, conn):
    cur = conn.cursor()
    ImprimirTitulo("Publicacion #{}".format(idPublicacion))
    cur.execute(verPublicacion.format(idPublicacion))
    contenidoPublicacion = cur.fetchall()
    ImprimirInfoPublicacion(contenidoPublicacion)
    ImprimirComentarios(idPublicacion, conn)
    opciones = ["Volver", "Salir"]
    ImprimirOpciones(opciones)
    seleccion = ValidarOpcion([1,2])
    if seleccion == 1:
        cur.close()
        return
    elif seleccion == 2:
        cur.close()
        sys.exit()
    return


def EliminarPublicacion(idPublicacion, conn):
    cur = conn.cursor()
    cur.execute(eliminarPublicacion.format(idPublicacion))
    Imprimir("Publicacion eliminada.")
    cur.close()
    conn.commit()
    return


def Comentar(idPublicacion, conn, nombre, idComentado = None):
    cur = conn.cursor()
    cur.execute("SELECT id FROM publicacion ORDER BY id DESC LIMIT 1")
    id = cur.fetchall()
    id = id[0][0]+1
    ImprimirTitulo("Comentar.")
    fecha = "{:%d-%m-%Y}".format(datetime.date.today())
    contenido = PedirDescripcion("comentario")
    borrado = False
    cur.execute(comentar.format(id, idComentado, nombre, idPublicacion, contenido, fecha, borrado))
    cur.close()
    conn.commit()
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
