from datetime import date
from IO import *
email = ""
password = ""

def PedirMail():
    __email = input("Correo: ")
    while __email == "" or not (re.match(".*@.*\..*", __email)):
        __email = input("Error, ingrese un correo valido: ")
    return __email


def PedirPassword():
    __password = input("Contraseña: ")
    while __password == "":
        __password = input("Error, ingrese una password valida: ")
    return __password


def IngresarDatos():
    _email = PedirMail()
    _password = PedirPassword()
    return _email, _password


def Confirmar():
    Imprimir("CONFIRMAR DATOS")
    #Imprimir("{:<10} {:>10}\n{:<10} {:>10}".format("Correo:", email, "Password:", password))
    _confirm = ""
    while not (re.match("[10]", _confirm)):
        _confirm = input("\t(0) Cambiar datos\n\t(1) Todo OK\nIngrese su opcion: ")
    return _confirm

def CrearCuenta(conn):
    cur = conn.cursor()
    cur.execute("select * from contrasena_antigua")
    ca = cur.fetchall()
    dicCorreoContra = {}
    dicCorreoId = {}
    for tupla in ca:
        dicCorreoContra[tupla[1]] = tupla[2]
        dicCorreoId[tupla[1]] = tupla[0]

    idNuevo = max(dicCorreoId.values()) + 1
    fechaActual = date.today()

    Imprimir("CREAR CUENTA")
    email, password = IngresarDatos()
    confirm = Confirmar()
    while confirm == "0" or confirm != "1":
        Imprimir("CAMBIAR DATOS")
        email, password = IngresarDatos()
        confirm = Confirmar()
    Imprimir("VERIFICACION DE CONTRASEÑA")
    verifPassword = input("Ingrese la contraseña nuevamente: ")
    while verifPassword != password:
        verifPassword = input("Contraseñas no coinciden, intente nuevamente: ")

    #print("Insertando un usuario con los siguientes datos:"
    #      "\nCorreo:", email,
    #      "\nContraseña:", password)

    cur.execute("insert into usuario(correo) values('{}');".format(email))
    cur.execute("insert into contrasena_antigua(id, correo_usuario, contrasena, fecha_creacion) "
                "values({},'{}','{}','{}');".format(idNuevo, email, password, fechaActual))
    conn.commit()
    cur.close()
