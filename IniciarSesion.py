
def iniciar_sesion(conn):
    cur = conn.cursor()
    cur.execute("select * from contrasena_antigua")
    ca = cur.fetchall()
    dic_correo_contra = {}
    for tupla in ca:
        dic_correo_contra[tupla[1]] = tupla[2]
    correo = input("Ingrese su correo electronico: ")
    while correo not in dic_correo_contra.keys():
        correo = input("Correo no valido, ingreselo nuevamente: ")
    contra = input("Ingrese su contrasena: ")
    while contra != dic_correo_contra[correo]:
        contra = input("Contrasena incorrecta, ingresela nuevamente: ")
    return correo
