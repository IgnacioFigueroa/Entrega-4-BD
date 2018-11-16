from IO import *
from tabulate import *
import datetime
#----QUERYS------
NombresEmpresas = "SELECT e.nombre, e.id " \
                  "FROM administrador a, empresa e " \
                  "WHERE a.id_empresa = e.id " \
                  "AND a.correo_usuario = '{}' " \
                  "AND a.activo = TRUE;"

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

comentarEmpresa = "INSERT INTO comentario (id, id_comentado, empresa_comentadora, id_publicacion, contenido, fecha, borrado) " \
           "VALUES ({},{},'{}',{},'{}',TO_DATE('{}', 'DD/MM/YYYY'),{});"

getTrabajadores = "SELECT p.id, p.correo_usuario " \
                  "FROM trabajado, trabajo, perfil p " \
                  "WHERE trabajado.id_trabajo = trabajo.id " \
                  "AND trabajado.id_perfil = p.id " \
                  "AND trabajo.id_empresa = {} " \
                  "AND (trabajado.fecha_termino > TO_DATE('{}', 'DD/MM/YYYY') " \
                  "OR trabajado.fecha_termino IS NULL);"

agregarAdmin = "INSERT INTO administrador (id, id_empresa, correo_usuario, Activo) " \
               "VALUES ({}, {}, '{}', {});"

obtenerAdministradores = "SELECT COUNT(*) c FROM administrador WHERE id_empresa = {} AND activo = TRUE;"

dejarDeSerAdmin = "UPDATE administrador SET activo = FALSE WHERE correo_usuario = '{}'"

crearEmpresa = "INSERT INTO empresa (id, nombre, fecha_creacion, pais, rubro, descripcion) " \
               "VALUES ({}, '{}', TO_DATE('{}', 'DD/MM/YYYY'), '{}', '{}', '{}')"

eliminarEmpresa = "DELETE FROM empresa WHERE id = {};"

empresasQueOfrecenTrabajos = "SELECT e.id, e.nombre, COUNT(*) trabajosOfrecidos FROM empresa e, trabajo t WHERE e.id = t.id_empresa " \
                             "AND t.postulacion_abierta = TRUE " \
                             "GROUP BY e.id, e.nombre " \
                             "ORDER BY e.id "

ultimasPublicaciones = "SELECT texto, foto, link, fecha FROM publicacion WHERE id_empresa = {} " \
                       "AND estado = 'publica' " \
                       "ORDER BY fecha DESC LIMIT {};"

ultimosComentarios = "SELECT c.contenido, c.fecha FROM comentario c, publicacion p WHERE c.empresa_comentadora = {} " \
                     "AND c.id_publicacion = p.id AND p.estado = 'publica' " \
                     "ORDER BY c.fecha DESC LIMIT {};"

trabajosOfrecidos = "SELECT id, descripcion, fecha_creacion FROM trabajo WHERE id_empresa = {} " \
                    "AND postulacion_abierta = TRUE;"

obtenerInfoTrabajoOfrecido = "SELECT t.id, t.id_empresa, e.nombre, t.descripcion, t.fecha_creacion, t.postulacion_abierta " \
                             "FROM trabajo t, empresa e WHERE t.id = {} AND t.id_empresa = e.id;"

postulantes = "SELECT COUNT(*) c FROM postulacion WHERE estado = 'pendiente' AND id_trabajo = {}"

crearPostulacion = ("INSERT INTO postulacion (id, correo_usuario, id_trabajo, estado, fecha) "
                    "VALUES ({}, '{}', {}, '{}', TO_DATE('{}', 'DD/MM/YYYY'))")

# Recibe el correo_usuario en usuario
def MenuEmpresas(usuario, conn):
    ImprimirTitulo("EMPRESAS")
    #seleccionar ver mis empresas o ver otros trabajos
    opciones = ["Empresas que soy administrador",
               "Ver trabajos",
               "Salir"]
    ImprimirOpciones(opciones)
    seleccion = ValidarOpcion(range(1,len(opciones)+1))
    if seleccion == 3:
        sys.exit(0)
    elif seleccion == 1:
        MostrarMisEmpresas(usuario, conn)
    elif seleccion == 2:
        VerTrabajos2(usuario, conn)
    return


def MostrarMisEmpresas(usuario, conn):
    ImprimirTitulo("Mis Empresas")
    cur = conn.cursor()
    cur.execute(NombresEmpresas.format(usuario))
    empresas = cur.fetchall()
    administraEmpresas = True
    if len(empresas)<1:
        administraEmpresas = False
    if administraEmpresas:
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
                          "Agregar administrador",
                          "Dejar de ser administrador",
                          "Crear empresas",
                          "Eliminar empresas",
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
            MostrarMisEmpresas(usuario, conn)
        elif seleccion == 5:
            DejarDeSerAdministrador(usuario, idEmpresaSeleccionada, conn)
            MostrarMisEmpresas(usuario, conn)
        elif seleccion == 6:
            CrearEmpresa(usuario, conn)
            MostrarMisEmpresas(usuario, conn)
        elif seleccion == 7:
            EliminarEmpresa(idEmpresaSeleccionada, conn)
            MostrarMisEmpresas(usuario, conn)
        elif seleccion == 8:
            MenuEmpresas(usuario, conn)

    elif administraEmpresas == False:
        Imprimir("Mostrando opciones limitadas ya que no administras ninguna empresa")
        opcionesEmpresa = ["Crear empresas",
                           "Volver",
                           "Salir"]
        ImprimirOpciones(opcionesEmpresa)
        cur.close()
        seleccion = ValidarOpcion(range(1,len(opcionesEmpresa)+1))
        if seleccion == 1:
            CrearEmpresa(usuario, conn)
            MenuEmpresas(usuario, conn)
        elif seleccion == 2:
            MenuEmpresas(usuario, conn)
        elif seleccion == 3:
            conn.close()
            sys.exit()
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
    if len(trabajos)<1:
        Imprimir("Mostrando opciones modificadas por falta de trabajos.")
        Imprimir("({}) Agregar trabajos".format(i))
        i+=1
    opciones = "({}) Volver.\n" \
               "({}) Salir.".format(i, i+1)
    Imprimir(opciones)
    seleccion = ValidarOpcion(range(1, i+2), "Seleccione un trabajo: ")
    cur.close()
    if len(trabajos)<1:
        if seleccion == 1:
            AgregarTrabajos(idEmpresa, conn)
            VerTrabajos1(idEmpresa, conn)
        elif seleccion == 2:
            return
        elif seleccion == 3:
            cur.close()
            conn.close()
            sys.exit()
    else:
        if seleccion == i:
            return
        elif seleccion == i+1:
            sys.exit()
        else:
            idTrabajo = trabajos[seleccion-1]
            opciones = ["Ver trabajo",
                        "Abrir postulaciones",
                        "Cerrar postulaciones",
                        "Agregar trabajos",
                        "Eliminar trabajo",
                        "Volver",
                        "Salir"]
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
                conn.close()
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
    idsComentarios = ImprimirComentarios(idPublicacionSeleccionada, conn)

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
        Comentar(idPublicacionSeleccionada, conn, nombreEmpresa, idsComentarios)
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
    conn.commit()
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


def Comentar(idPublicacion, conn, nombre, idsComentarios):
    cur = conn.cursor()
    id = SiguienteID("Comentario", conn)
    ImprimirTitulo("Comentar.")
    fecha = "{:%d-%m-%Y}".format(datetime.date.today())
    idsComentarios.append(0)
    idComentado = ValidarOpcion(idsComentarios,"(0)  Comentar en la publicacion.\n"
                                               "(id) Ingrese un id de otro comentario para comentarlo."
                                               "Ingrese su opcion: ")
    if (idComentado==0):
        idComentado = "NULL"
    contenido = PedirDescripcion("comentario")
    borrado = False
    cur.execute(comentarEmpresa.format(id, idComentado, nombre, idPublicacion, contenido, fecha, borrado))
    cur.close()
    conn.commit()
    return


def AgregarAdministrador(idEmpresa, conn):
    cur = conn.cursor()
    fecha = "{:%d-%m-%Y}".format(datetime.date.today())
    cur.execute(getTrabajadores.format(idEmpresa,fecha))
    trabajadoresActivos = cur.fetchall()
    ImprimirTitulo("Seleccionar trabajador.")
    Imprimir(tabulate(trabajadoresActivos, showindex=range(1,len(trabajadoresActivos)+1)))
    i = len(trabajadoresActivos)+1
    if len(trabajadoresActivos)<1:
        Imprimir("No hay trabajadores. :(")
    Imprimir("{} Volver.\n"
             "{} Salir.".format(i,i+1))
    seleccion = ValidarOpcion(range(1, i+3))
    if seleccion == i:
        return
    elif seleccion == i+1:
        conn.close()
        sys.exit()
    id = SiguienteID("administrador", conn)
    correo_usuario = trabajadoresActivos[seleccion-1][1]
    Activo = True
    cur.execute(agregarAdmin.format(id, idEmpresa, correo_usuario, Activo))
    Imprimir("Administrador agregado.")
    conn.commit()
    cur.close()
    return


def DejarDeSerAdministrador(correoUsuario, IdEmpresa, conn):
    cur = conn.cursor()
    cur.execute(obtenerAdministradores.format(IdEmpresa))
    cantidadAdministradores = cur.fetchall()
    cantidadAdministradores = cantidadAdministradores[0][0]
    if cantidadAdministradores<2:
        Imprimir("Irte no puedes, el ultimo jedi (administrador) eres... .")
    else:
        cur.execute(dejarDeSerAdmin.format(correoUsuario))
        Imprimir("Cobarde... Ya no eres administrador")
        conn.commit()
    cur.close()
    return


def CrearEmpresa(usuario, conn):
    cur = conn.cursor()
    ImprimirTitulo("Crear empresa.")
    id = SiguienteID("empresa", conn)
    nombre = PedirUnaLinea("Ingrese el nombre de la empresa: ")
    fecha = "{:%d-%m-%Y}".format(datetime.date.today())
    pais = PedirUnaLinea("Pais: ")
    rubro = PedirUnaLinea("Rubro: ")
    descripcion = PedirDescripcion("descripcion de la empresa")
    # query crear empresa
    cur.execute(crearEmpresa.format(id, nombre, fecha, pais, rubro, descripcion))
    # query agregar admin
    idAdmin = SiguienteID("administrador", conn)
    cur.execute(agregarAdmin.format(idAdmin, id, usuario, True))
    Imprimir("Epresa creada con exito. Ya eres administrador de la empresa '{}'".format(nombre))
    conn.commit()
    cur.close()
    return


def EliminarEmpresa(idEmpresa, conn):
    cur = conn.cursor()
    cur.execute("SELECT nombre FROM empresa WHERE id = {}".format(idEmpresa))
    nombreEmpresa = cur.fetchall()
    nombreEmpresa = nombreEmpresa[0][0]
    ImprimirTitulo("Eliminar empresa")
    Imprimir("Esta seguro que desea eliminar la empresa '{}' ?".format(nombreEmpresa))
    ImprimirOpciones(["Si", "No"])
    seleccion = ValidarOpcion(range(1,3))
    if seleccion == 1:
        cur.execute(eliminarEmpresa.format(idEmpresa))
        conn.commit()
    else:
        Imprimir("No se eliminara.")
    cur.close()
    return


def VerTrabajos2(usuario, conn):
    cur = conn.cursor()
    ImprimirTitulo("Ver Trabajos")
    cur.execute(empresasQueOfrecenTrabajos)
    trabajosDisponibles = cur.fetchall()
    cantidad_ofertas = len(trabajosDisponibles)
    Imprimir(tabulate(trabajosDisponibles, headers=["Id empresa", "Nombre empresa", "Trabajos ofrecidos"],showindex=range(1,cantidad_ofertas+1)))
    Imprimir("{} Volver\n{} Salir".format(cantidad_ofertas+1, cantidad_ofertas+2))
    seleccion = ValidarOpcion(range(1, cantidad_ofertas+3))
    if seleccion == cantidad_ofertas+1:
        return
    elif seleccion == cantidad_ofertas+2:
        cur.close()
        conn.close()
        sys.exit()
    else:
        idTrabajoSeleccionado = trabajosDisponibles[seleccion-1][0]
        opciones = ["Ver empresa",
                    "Volver",
                    "Salir"]
        ImprimirOpciones(opciones)
        seleccion = ValidarOpcion(range(1,4))
        if seleccion == 1:
            VerEmpresa(idTrabajoSeleccionado, usuario, conn)
        elif seleccion == 2:
            cur.close()
            VerTrabajos2(idTrabajoSeleccionado, conn)
        elif seleccion == 3:
            cur.close()
            conn.close()
            sys.exit()
    return


def VerEmpresa(idEmpresa, correoUsuario, conn):
    cur = conn.cursor()
    cur.execute(ultimasPublicaciones.format(idEmpresa,5))
    UltimasPublicaciones = cur.fetchall()
    cur.execute(ultimosComentarios.format(idEmpresa,2))
    UltimosComentarios = cur.fetchall()
    cur.execute(trabajosOfrecidos.format(idEmpresa))
    TrabajosOfrecidos = cur.fetchall()
    ImprimirTitulo("Ultimas publicaciones:")
    if(len(UltimasPublicaciones)<1):
        Imprimir("No hay publicaciones")
    else:
        Imprimir(tabulate(UltimasPublicaciones, headers=["Contenido", "Foto", "Link", "Fecha publicacion"]))
    ImprimirTitulo("Ultimos comentarios:")
    if len(UltimosComentarios)<1:
        Imprimir("No hay comentarios")
    else:
        Imprimir(tabulate(UltimosComentarios, headers=["id", "Descripcion", "Fecha creacion"]))
    ImprimirTitulo("Trabajos ofrecidos:")
    int_trabajosOfrecidos = len(TrabajosOfrecidos)
    Imprimir(tabulate(TrabajosOfrecidos, showindex=range(1, int_trabajosOfrecidos+1), headers=["id", "Descripcion", "Fecha creacion"]))
    Imprimir("{} Volver.\n{} Salir.".format(int_trabajosOfrecidos+1, int_trabajosOfrecidos+2))
    seleccion = ValidarOpcion(range(1, int_trabajosOfrecidos+3))
    if seleccion == int_trabajosOfrecidos+1:
        return
    elif seleccion == int_trabajosOfrecidos+2:
        cur.close()
        conn.close()
        sys.exit()
    else:
        idTrabajoSeleccionado = TrabajosOfrecidos[seleccion-1][0]
        opciones = ["Ver trabajo",
                    "Postular",
                    "Volver",
                    "Salir"]
        ImprimirOpciones(opciones)
        seleccion = ValidarOpcion(range(1,5))
        if seleccion == 1:
            VerTrabajo2(idTrabajoSeleccionado, conn)
            VerEmpresa(idEmpresa, correoUsuario, conn)
        elif seleccion == 2:
            PostularTrabajo(idTrabajoSeleccionado, correoUsuario, conn)
            VerEmpresa(idEmpresa, correoUsuario, conn)
    return


def VerTrabajo2(idTrabajo, conn):
    cur = conn.cursor()
    ImprimirTitulo("Ver trabajo")
    cur.execute(obtenerInfoTrabajoOfrecido.format(idTrabajo))
    infoTrabajo = cur.fetchall()
    cur.execute(postulantes.format(idTrabajo))
    cantidad_postulantes = cur.fetchall()
    cantidad_postulantes = cantidad_postulantes[0][0]
    info1 = []
    for i in infoTrabajo[0]:
        info1.append(i)
    info1.append(cantidad_postulantes)
    info = [info1]
    Imprimir(tabulate(info, headers=["Id", "Id Empresa", "Nombre Empresa", "Descripcion", "Fecha creacion", "Postulaciones abiertas", "Cantidad postulantes"], tablefmt = 'grid'))
    return


def PostularTrabajo(idTrabajo, correoUsuario, conn):
    ImprimirTitulo("Postular a trabajo")
    cur = conn.cursor()
    id = SiguienteID("postulacion", conn)
    estado = 'pendiente'
    fecha = "{:%d-%m-%Y}".format(datetime.date.today())
    cur.execute(crearPostulacion.format(id, correoUsuario, idTrabajo, estado, fecha))
    Imprimir("Postulacion realizada con exito.")
    conn.commit()
    cur.close()
    return
