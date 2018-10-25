import sys

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
    ids_comentariosPresentes = []
    for comentario in comentarios_query:
        ids_comentariosPresentes.append(comentario[0])
    autor = comentario[2]
    if autor == None:
        autor = comentario[7]
    result = "{:<4}> {:%d-%m-%Y} | {} dijo: {}".format(comentario[0], comentario[5], autor, comentario[4])
    print(result)

    """
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
    """
    return ids_comentariosPresentes

"""
def ImprimirComentario(comment, indent=0):
    id = comment["Comentario"][0]
    fecha = comment["Comentario"][5]
    autor = comment["Comentario"][2]
    if autor == None:
        autor = comment["Comentario"][7]
    texto = comment["Comentario"][4]
    print ("{:<3}{:%d-%m-%Y}  ".format(id,fecha)+"\t"*indent+"|{} dijo: {}".format(autor, texto))
    for sub_com in comment["Comentarios"]:
        indent += 1
        ImprimirComentario(sub_com, indent)
"""

def HayConexionBD(conn):
    if "closed: 0" in str(conn): # si esta conectado
        return True
    elif "closed: 1" in str(conn): # no esta conectado
        return False
