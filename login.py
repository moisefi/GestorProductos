import os
from proveedor import *
from usuario import *
from admin import *
# He utilizado .pack() en esta parte del proyecto por probar algo nuevo y funciona bastante bien
# Creo 3 variables que luego me serviran para identificar quien se ha logeado si admin, usuario o proveedor
entrar_admin = False
entrar_usuario = False
entrar_proveedor = False
# No voy a comentar mucho las ventanas porque creo que han quedado bastante bien organizadas y me voy a repetir
# La ventana principal tendra 3 botones, acceder y registro ( para usuarios ) y para proveedores
def ventana_inicio():
    global ventana_principal
    pestas_color = "DarkGrey"
    ventana_principal = Tk()
    ventana_principal.geometry("300x250")
    ventana_principal.title("El mercadillo de Sergio")
    ventana_principal.wm_iconbitmap("recursos/icon.ico")
    Label(text="Escoja su opción", bg="LightGreen", width="300", height="2", font=("Calibri, 13")).pack()
    Label(text="").pack()
    Button(text="Acceder", height="2", width="30", bg=pestas_color, command=login).pack()
    Label(text="").pack()
    Button(text="Registrarse", height="2", width="30", bg=pestas_color, command=registro).pack()
    Label(text="").pack()
    Button(text="Para Proveedores", height=2, width="30", bg=pestas_color, command=proveedores).pack()
    ventana_principal.mainloop()
# Esta ventana tendra 2 botones uno de acceder y otro de registro para los proveedores
def proveedores():
    global ventana_proveedores
    pestas_color = "DarkGrey"
    ventana_proveedores = Toplevel(ventana_principal)
    ventana_proveedores.title("Proveedores")
    ventana_proveedores.geometry("300x250")
    ventana_proveedores.wm_iconbitmap("recursos/icon.ico")
    Label(ventana_proveedores, text="Escoja su opción", bg="LightGreen", width="300", height="2", font=("Calibri, 13")).pack()
    Label(ventana_proveedores, text="").pack()
    Button(ventana_proveedores, text="Acceder", height="2", width="30", bg=pestas_color, command=login_proveedores).pack()
    Label(ventana_proveedores, text="").pack()
    Button(ventana_proveedores, text="Registrarse", height="2", width="30", bg=pestas_color, command=registro_proveedores).pack()
    Label(ventana_proveedores, text="").pack()

def login_proveedores():
    global ventana_login_proveedores
    global verifica_proveedor
    global verifica_contrasena
    global verifica_login_proveedores
    global mensajep
    # Es importante definir estas variables como stringvar o intvar para trabajar luego con ellas
    verifica_proveedor = StringVar()
    verifica_contrasena = StringVar()

    ventana_login_proveedores = Toplevel(ventana_principal)
    ventana_login_proveedores.title("Login Proveedores")
    ventana_login_proveedores.geometry("300x250")
    ventana_login_proveedores.wm_iconbitmap("recursos/icon.ico")

    Label(ventana_login_proveedores, text="Introduzca nombre de usuario y contraseña").pack()
    Label(ventana_login_proveedores, text="").pack()

    Label(ventana_login_proveedores, text="Usuario del proveedor").pack()
    entrada_login_proveedores = Entry(ventana_login_proveedores, textvariable=verifica_proveedor)
    entrada_login_proveedores.pack()
    Label(ventana_login_proveedores, text="").pack()
    Label(ventana_login_proveedores, text="Contraseña").pack()
    entrada_login_contrasena = Entry(ventana_login_proveedores, textvariable=verifica_contrasena, show='*')
    entrada_login_contrasena.pack()
    Label(ventana_login_proveedores, text="").pack()
    Button(ventana_login_proveedores, text="Acceder", width=10, height=1, command=verifica_login_proveedores).pack()
    mensajep = Label(ventana_login_proveedores, text="", fg="red")
    mensajep.pack()
# La consulta de la base de datos de proveedores
def dbp_consulta(consulta, parametros=()):
    with sqlite3.connect(dbp) as con:
        cursor = con.cursor()
        resultado = cursor.execute(consulta, parametros)
        con.commit()
    return resultado

def verifica_login_proveedores():
    global usuario_p
    global contrasena_p
    global mensajep
    global entrar_proveedor
    # Cojo los datos que han introducido para usuario y contraseña
    usuario_p = verifica_proveedor.get()
    contrasena_p = verifica_contrasena.get()

    # Si buscando en la base de datos por ese usuario y contraseña un nombre de empresa me da 1 de resultado es que estan correctos
    # Ponemos en True la entrada de proveedor
    query = "SELECT nombre_empresa FROM proveedores WHERE usuario=(?) and contrasena=(?)"
    parametros = (usuario_p, contrasena_p,)
    conexion = sqlite3.connect('database/proveedores.db')
    cursor = conexion.cursor()
    cursor.execute(query,(parametros))
    datos = cursor.fetchall()

    if len(datos) == 1:
        entrar_proveedor = True
        ventana_principal.destroy()
    else:
        mensajep["text"] = "Los datos introducidos no son correctos"
    conexion.close()

# Recojo todos los datos del registro de proveedores
def registro_proveedores():
    global ventana_registro_proveedores
    global dbp
    global nombre_empresa
    global telefono
    global direccion
    global cif
    global email
    global usuario
    global contrasena
    global mensaje
    global intro_nombre_empresa
    global intro_telefono
    global intro_direccion
    global intro_cif
    global intro_email
    global intro_usuario
    global intro_contrasena
    pestas_color = "DarkGrey"
    dbp = "database/proveedores.db"
    ventana_registro_proveedores = Toplevel(ventana_principal)
    ventana_registro_proveedores.title("Registro Proveedores")
    ventana_registro_proveedores.geometry("350x500")
    ventana_registro_proveedores.wm_iconbitmap("recursos/icon.ico")

    nombre_empresa = StringVar()
    telefono = IntVar()
    direccion = StringVar()
    cif = StringVar()
    email = StringVar()
    usuario = StringVar()
    contrasena = StringVar()

    # Label y Entry del nombre de la empresa
    etiqueta_nombre_empresa = Label(ventana_registro_proveedores, text="Escriba el nombre de su empresa", bg="LightGreen").pack()
    intro_nombre_empresa = Entry(ventana_registro_proveedores, textvariable=nombre_empresa)
    intro_nombre_empresa.pack()
    Label(ventana_registro_proveedores, text="").pack()

    # Label y Entry del telefono
    etiqueta_telefono = Label(ventana_registro_proveedores, text="Introduzca su número de telefono", bg="LightGreen").pack()
    intro_telefono = Entry(ventana_registro_proveedores, textvariable=telefono)
    intro_telefono.pack()
    Label(ventana_registro_proveedores, text="").pack()

    # Label y Entry de la direccion
    etiqueta_direccion = Label(ventana_registro_proveedores, text="Introduzca la dirección de la empresa", bg="LightGreen").pack()
    intro_direccion = Entry(ventana_registro_proveedores, textvariable=direccion)
    intro_direccion.pack()
    Label(ventana_registro_proveedores, text="").pack()

    # Label y Entry del CIF
    etiqueta_cif = Label(ventana_registro_proveedores, text="Ponga el CIF completo", bg="LightGreen").pack()
    intro_cif = Entry(ventana_registro_proveedores, textvariable=cif)
    intro_cif.pack()
    Label(ventana_registro_proveedores, text="").pack()

    #Label y Entry del email
    etiqueta_email = Label(ventana_registro_proveedores, text="Agregue un email de contacto", bg="LightGreen").pack()
    intro_email = Entry(ventana_registro_proveedores, textvariable=email)
    intro_email.pack()
    Label(ventana_registro_proveedores, text="").pack()

    # Label y Entry usuario
    etiqueta_usuario = Label(ventana_registro_proveedores, text="Escoja su nombre de usuario para ingresar en la plataforma", bg="LightGreen").pack()
    intro_usuario = Entry(ventana_registro_proveedores, textvariable=usuario)
    intro_usuario.pack()
    Label(ventana_registro_proveedores, text="").pack()

    # Label y Entry contraseña
    etiqueta_contrasena = Label(ventana_registro_proveedores, text="Elija una contraseña", bg="LightGreen").pack()
    intro_contrasena = Entry(ventana_registro_proveedores, textvariable=contrasena, show='*')
    intro_contrasena.pack()
    Label(ventana_registro_proveedores, text="").pack()

    Button(ventana_registro_proveedores, text="Guardar Datos", command=add_proveedor).pack()
    mensaje = Label(ventana_registro_proveedores, text="", fg="red")
    mensaje.pack()
    return nombre_empresa
# Validaciones que me serviran para que no dejen campos en blanco
def validacion_nombre_empresa():
    nombre_empresa_introducido_usuario = nombre_empresa.get()
    return len(nombre_empresa_introducido_usuario) != 0
def validacion_direccion():
    direccion_introducida_usuario = direccion.get()
    return len(direccion_introducida_usuario) != 0
def validacion_telefono():
    telefono_introducido_usuario = telefono.get()
    return len(telefono_introducido_usuario) != 0
def validacion_cif():
    cif_introducido_usuario = cif.get()
    return len(cif_introducido_usuario) != 0
def validacion_email():
    email_introducido_usuario = email.get()
    return len(email_introducido_usuario)
def validacion_usuario():
    usuario_introducido_usuario = usuario.get()
    return len(usuario_introducido_usuario) != 0
def validacion_contrasena():
    contrasena_introducida_usuario = contrasena.get()
    return len(contrasena_introducida_usuario) != 0

def add_proveedor():
    global tabla_nombre_empresa
    # Cojo todos los datos que han introducido, si hay alguno en blanco les saldra el mensaje del else y sino rellenara los campos
    tabla_nombre_empresa = nombre_empresa.get()
    tabla_direccion = direccion.get()
    tabla_telefono = telefono.get()
    tabla_cif = cif.get()
    tabla_email = email.get()
    tabla_usuario = usuario.get()
    tabla_contrasena = contrasena.get()
    if validacion_nombre_empresa() and validacion_direccion() and validacion_telefono() and validacion_cif() and validacion_email() and validacion_usuario() and validacion_contrasena():
        query = "INSERT INTO proveedores VALUES( NULL, ?, ?, ?, ?, ?, ?, ?)"
        parametros = (tabla_nombre_empresa, tabla_telefono, tabla_direccion, tabla_cif, tabla_email, tabla_usuario, tabla_contrasena)
        dbp_consulta(query, parametros)
        mensaje["text"] = "La empresa {} ha sido registrada con éxito".format(nombre_empresa.get())
        intro_nombre_empresa.delete(0, END)  # Borrar el campo nombre
        intro_direccion.delete(0, END)  # Borrar el campo direccion
        intro_telefono.delete(0, END)  # Borrar el campo telefono
        intro_cif.delete(0, END)  # Borrar el campo cif
        intro_email.delete(0, END)  # Borrar el campo email
        intro_usuario.delete(0, END)  # Borrar el campo usuario
        intro_contrasena.delete(0, END)  # Borrar el campo contrasena
    else:
        mensaje["text"] = "Rellene todos los campos"


# El registro de usuarios es igual pero en vez de SQL utilizo documentos de texto
def registro():
    global ventana_registro
    ventana_registro = Toplevel(ventana_principal)
    ventana_registro.title("Registro")
    ventana_registro.geometry("300x250")
    ventana_registro.wm_iconbitmap("recursos/icon.ico")

    global nombre_usuario
    global clave
    global entrada_nombre
    global entrada_clave
    nombre_usuario = StringVar()
    clave = StringVar()

    Label(ventana_registro, text="Introduzca datos", bg="LightGreen").pack()
    Label(ventana_registro, text="").pack()
    etiqueta_nombre = Label(ventana_registro, text="Nombre usuario * ")
    etiqueta_nombre.pack()
    entrada_nombre = Entry(ventana_registro, textvariable=nombre_usuario)
    entrada_nombre.pack()
    etiqueta_clave = Label(ventana_registro, text="Contraseña * ")
    etiqueta_clave.pack()
    entrada_clave = Entry(ventana_registro, textvariable=clave, show='*')
    entrada_clave.pack()
    Label(ventana_registro, text="").pack()
    Button(ventana_registro, text="Registrarse", width=10, height=1, bg="LightGreen", command= registro_usuario).pack()

def registro_usuario():
    # Cojo los datos que han metido en el registro de usuarios y creo un documento de texto con ellos

    usuario_info = nombre_usuario.get()
    clave_info = clave.get()

    file = open(usuario_info, "w")
    file.write(usuario_info + "\n")
    file.write(clave_info)
    file.close()

    entrada_nombre.delete(0, END)
    entrada_clave.delete(0, END)

    Label(ventana_registro, text="Registro completado con éxito", fg="green", font=("calibri", 11)).pack()


def login():
    global  ventana_login
    ventana_login = Toplevel(ventana_principal)
    ventana_login.title("Acceso a la cuenta")
    ventana_login.geometry("300x250")
    ventana_login.wm_iconbitmap("recursos/icon.ico")
    Label(ventana_login, text="Introduzca nombre de usuario y contraseña").pack()
    Label(ventana_login, text="").pack()

    global verifica_usuario
    global verifica_clave

    verifica_usuario = StringVar()
    verifica_clave = StringVar()

    global entrada_login_usuario
    global entrada_login_clave

    Label(ventana_login, text="Nombre usuario").pack()
    entrada_login_usuario = Entry(ventana_login, textvariable=verifica_usuario)
    entrada_login_usuario.pack()
    Label(ventana_login, text="").pack()
    Label(ventana_login, text="Contraseña").pack()
    entrada_login_clave = Entry(ventana_login, textvariable=verifica_clave, show='*')
    entrada_login_clave.pack()
    Label(ventana_login, text="").pack()
    Button(ventana_login, text="Acceder", width=10, height=1, command= verifica_login).pack()

def verifica_login():
    global usuario1
    global clave1

    # Si la información introducida esta en algún documento de texto entonces podran logearse
    # Si no es correcta la informacion saldra o no clave o no usuario que son dos funciones hechas a continuación
    usuario1 = verifica_usuario.get()
    clave1 = verifica_clave.get()
    entrada_login_usuario.delete(0, END)
    entrada_login_clave.delete(0, END)

    lista_archivos = os.listdir()
    if usuario1 in lista_archivos:
        archivo1 = open(usuario1, "r")
        verifica = archivo1.read().splitlines()
        if clave1 in verifica:
            exito_login()
        else:
            no_clave()
    else:
        no_usuario()

def no_usuario():
    global ventana_no_usuario
    ventana_no_usuario = Toplevel(ventana_login)
    ventana_no_usuario.title("ERROR")
    ventana_no_usuario.geometry("150x100")
    ventana_no_usuario.wm_iconbitmap("recursos/icon.ico")
    Label(ventana_no_usuario, text="Usuario no encontrado").pack()
    Button(ventana_no_usuario, text="OK", command= borrar_no_usuario).pack()

def exito_login():
    global ventana_exito
    ventana_exito = Toplevel(ventana_login)
    ventana_exito.title("Éxito")
    ventana_exito.geometry("150x100")
    ventana_exito.wm_iconbitmap("recursos/icon.ico")
    Label(ventana_exito, text="Login finalizado con éxito").pack()
    Button(ventana_exito, text="OK", command= borrar_exito_login).pack()

def no_clave():
    global ventana_no_clave
    ventana_no_clave = Toplevel(ventana_login)
    ventana_no_clave.title("ERROR")
    ventana_no_clave.geometry("150x100")
    ventana_no_clave.wm_iconbitmap("recursos/icon.ico")
    Label(ventana_no_clave, text="Contraseña Incorrecta").pack()
    Button(ventana_no_clave, text="OK", command= borrar_no_clave).pack()

def borrar_exito_login():
    global entrar_admin
    global entrar_usuario
    # Cuando se han terminado de logear si el usuario y la contraseña son admin dara paso al modo administrador y sino al modo usuario
    # Cierro todas las ventanas
    ventana_exito.destroy()
    ventana_principal.destroy()
    if usuario1 == "admin" and clave1 == "admin":
        entrar_admin = True
    else:
        entrar_usuario = True

def borrar_no_clave():
    ventana_no_clave.destroy()

def borrar_no_usuario():
    ventana_no_usuario.destroy()

# Inicio la ventana de login
ventana_inicio()
# Dependiendo del login se activara un modo u otro
if entrar_admin == True:
    root = Tk()
    app = Admin(root)
    root.mainloop()

elif entrar_usuario == True:
    root = Tk()
    app = Ventas(root)
    root.mainloop()

elif entrar_proveedor == True:
    root = Tk()
    usuario_proveedor = usuario_p
    app = Producto(root)
    root.mainloop()



