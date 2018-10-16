import re

email = ""
password = ""

def pedir_mail():
    __email = input("Email: ")
    while __email=="" or not (re.match(".*@.*\..*", __email)):
        __email = input("Email: ")
    return __email
        
def pedir_password():
    __password = input("Password: ")
    while __password == "":
        __password = input("Password: ")
    return __password

def ingresar_datos():
    _email = pedir_mail()
    _password = pedir_password()
    return _email,_password

def confirmar():
    print ("Confirmar los datos:")
    print ("{:<10} {:>10}\n{:<10} {:>10}".format("Mail:", email, "Password:", password))
    _confirm = ""
    while not(re.match("[10]",_confirm)):
        _confirm = input("0: cambiar datos. 1: todo ok\nSeleccion: ")
    return _confirm

print ("Agregar cuenta:")
email, password = ingresar_datos()
confirm = confirmar()
while confirm == "0" or confirm!= "1":
    print ("Cambiar datos.")
    email, password = ingresar_datos()
    confirm = confirmar()
    
