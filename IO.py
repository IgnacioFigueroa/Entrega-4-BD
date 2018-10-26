import sys
from tabulate import tabulate
VER_PERFIL = "SELECT * FROM Perfil WHERE correo_usuario = '{}' "
VER_ESTUDIOS = "SELECT em.nombre, e.grado_academico, e.descripcion, e.fecha_inicio, e.fecha_termino " \
               "FROM Estudio e JOIN Empresa em ON e.id_empresa = em.id " \
               "WHERE correo_usuario = '{}'"
VER_TRABAJOS = "SELECT e.nombre, t.descripcion, tr.fecha_inicio, tr.fecha_termino" \
               " FROM " \
               "Trabajo t JOIN Empresa e ON t.id_empresa = e.id " \
               "JOIN Trabajado tr ON t.id = tr.id_trabajo " \
               "JOIN Perfil p ON p.id = tr.id_perfil" \
               " WHERE p.correo_usuario = '{}'"
VER_HABILIDADES = "SELECT h.nombre, COUNT(v.id_perfil_habilidad) " \
                  "FROM Habilidad h JOIN Perfil_habilidad pf ON h.id = pf.id_habilidad " \
                  "JOIN Perfil p ON p.id=pf.id_perfil " \
                  "LEFT JOIN Validacion v ON pf.id = v.id_perfil_habilidad " \
                  "WHERE p.correo_usuario = '{}' " \
                  "GROUP BY h.nombre"
def VerPerfilHastaHabilidad(usuario, conn):
    cur = conn.cursor()
    cur.execute(VER_PERFIL.format(usuario))
    perfilPorVer = cur.fetchall()[0]
    atributosPerfil = ["Correo", "Nombre", "Apellido", "Fecha de Nacimiento", "Pais", "Sexo", "Descripcion"]
    tablaPerfil = list()
    for i in range(len(atributosPerfil)):
        tablaPerfil.append([atributosPerfil[i], perfilPorVer[i + 1]])
    Imprimir("PERFIL")
    Imprimir(tabulate(tablaPerfil))

    cur.execute(VER_ESTUDIOS.format(usuario))
    estudios = cur.fetchall()
    tablaEstudios = list()
    atributosEstudios = ["Universidad", "GradoAcademico", "Descripcion", "FechaInicio", "FechaTermino"]
    Imprimir("ESTUDIOS")
    for estudio in estudios:
        for i in range(len(estudio)):
            tablaEstudios.append([atributosEstudios[i], estudio[i]])
        Imprimir(tabulate(tablaEstudios))
        tablaEstudios = list()
    cur.execute(VER_TRABAJOS.format(usuario))
    trabajos = cur.fetchall()
    tablaTrabajos = list()
    atributosTrabajo = ["Empresa", "Descripcion del trabajo", "Fecha inicio", "Fecha termino"]
    Imprimir("TRABAJOS")
    for trabajo in trabajos:
        for i in range(len(trabajo)):
            tablaTrabajos.append([atributosTrabajo[i], trabajo[i]])
        Imprimir(tabulate(tablaTrabajos))
        tablaTrabajos = list()

    cur.execute(VER_HABILIDADES.format(usuario))
    habilidades = cur.fetchall()
    tablaHabilidades = list()
    atributosHabilidades = ["Habilidad", "Cantidad de validaciones"]
    Imprimir("HABILIDADES Y SUS VALIDACIONES")
    for habilidad in habilidades:
        for i in range(len(habilidad)):
            tablaHabilidades.append([atributosHabilidades[i], habilidad[i]])
        Imprimir(tabulate(tablaHabilidades))
        tablaHabilidades = list()

    return

def Imprimir(mensaje):
    print(mensaje)

def ImprimirTitulo(titulo):
    linea = "     "
    for i in range(len(titulo)):
        linea = linea + "_"
    print(linea)
    print("     " + titulo)
    print()

def ImprimirError(mensaje):
    print(mensaje)

def ImprimirPositivo(mensaje):
    print(mensaje)

def SiguienteID(tabla, conn, id="id"):
    cur = conn.cursor()
    cur.execute("SELECT {} FROM {} WHERE {} IS NOT null".format(id,tabla, id))
    rows = cur.fetchall()
    ids = list()
    for i in rows:
        ids.append(i[0])
    return max(ids)+1
def ValidarOpcion(rango, mensaje = "Ingrese su opcion: "):
    opcion = input(mensaje)
    patron = []
    for a in rango:
        patron.append(str(a))
    while not (opcion in patron):
        ImprimirError("Ingrese una opcion valida")
        opcion = input(mensaje)
    return int(opcion)

def ImprimirOpciones(listaOpciones, titulo = ""):
    i = 1
    stringOpciones = titulo
    for a in listaOpciones:
        stringOpciones += "\n({}) {}.".format(i,a)
        i += 1
    print (stringOpciones)

def PedirDescripcion(arg = "descripcion"):
    Imprimir("Ingrese {}. Use doble espacio para terminar".format(arg))
    texto = ""
    n_text = " "
    while len(n_text) != 0:
        n_text = input()
        texto += n_text + "\n"
    return texto

def ImprimirInfoPublicacion(publicacionCompleta):
    publicacion = publicacionCompleta[0]
    id = publicacion[0]
    if publicacion[1] == None:
        autor = publicacion[2]
    else:
        autor = publicacion[1]
    texto = publicacion[3]
    foto = publicacion [4]
    link = publicacion[5]
    tipo = publicacion[6]
    fecha = publicacion[7]
    borrada = publicacion[8]
    print ("ID: {:<4} Id/Correo autor: {}\n"
           "Texto:\n"
           "{}\n"
           "Foto: {}\n"
           "Link: {}\n"
           "Tipo: {}\n"
           "Fecha: {:%d-%m-%Y}\n"
           "Borrada: {}".format(id,autor,texto,foto,link,tipo,fecha,borrada))

def ImprimirComentarios(idPublicacion, conn):
    Imprimir("__________\nComentarios")
    cur = conn.cursor()
    cur.execute("SELECT * FROM comentario WHERE id_publicacion = {};".format(idPublicacion))
    comentarios_query = cur.fetchall()
    comentarios = []
    comentarios_de_comentarios = []
    ids_comentariosPresentes = []
    for comment in comentarios_query:
        comentario = {"Comentario":[],"Comentarios":[]}
        comentario["Comentario"] = comment
        ids_comentariosPresentes.append(comment[0])
        if comment[1] == None:
            comentarios.append(comentario)
        else:
            comentarios_de_comentarios.append(comentario)
    while len(comentarios_de_comentarios)>0:
        for comment in comentarios:
            id_comm = comment["Comentario"][0]
            for i in range(len(comentarios_de_comentarios)):
                com = comentarios_de_comentarios[i]
                if id_comm == com["Comentario"][1]:
                    comment["Comentarios"].append(com)
                    comentarios_de_comentarios.pop(i)
                    i -= 1
    for comment in comentarios:
        ImprimirComentario(comment)
    return ids_comentariosPresentes

def ImprimirComentario(comment, indent=0):
    id = comment["Comentario"][0]
    fecha = comment["Comentario"][5]
    autor = comment["Comentario"][2]
    texto = comment["Comentario"][4]
    print ("{:<3}{:%d-%m-%Y}  ".format(id,fecha)+"\t"*indent+"|{} dijo: {}".format(autor, texto))
    for sub_com in comment["Comentarios"]:
        indent += 1
        ImprimirComentario(sub_com, indent)

def HayConexionBD(conn):
    if "closed: 0" in str(conn): # si esta conectado
        return True
    elif "closed: 1" in str(conn): # no esta conectado
        return False
