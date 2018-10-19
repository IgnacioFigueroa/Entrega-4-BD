import re
email = ""
password = ""

def PedirMail():
    __email = input("Email: ")
    while __email == "" or not (re.match(".*@.*\..*", __email)):
        __email = input("Email: ")
    return __email


def PedirPassword():
    __password = input("Password: ")
    while __password == "":
        __password = input("Password: ")
    return __password


def IngresarDatos():
    _email = PedirMail()
    _password = PedirPassword()
    return _email, _password


def Confirmar():
    print("Confirmar los datos:")
    print("{:<10} {:>10}\n{:<10} {:>10}".format("Mail:", email, "Password:", password))
    _confirm = ""
    while not (re.match("[10]", _confirm)):
        _confirm = input("0: cambiar datos. 1: todo ok\nSeleccion: ")
    return _confirm

def CrearCuenta(conn):
    print("Agregar cuenta:")
    email, password = IngresarDatos()
    confirm = Confirmar()
    while confirm == "0" or confirm != "1":
        print("Cambiar datos.")
        email, password = IngresarDatos()
        confirm = Confirmar()
