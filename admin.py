from tkinter import ttk
from tkinter import *
import sqlite3
from usuario import Ventas
# En este archivo lo que hago es generar una tabla para cada base de datos pero en este caso las dos estan completas
# Creo un boton para poder entrar en la ventana de usuario

class Admin:

    db = "database/producto.db"
    dbp = "database/proveedores.db"

    def __init__(self, root):
        self.ventana_a = root
        self.ventana_a.title("Modo Administrador")
        self.ventana_a.resizable(0,0)
        self.ventana_a.configure(background="cyan")
        self.ventana_a.wm_iconbitmap("recursos/icon.ico")

        self.etiqueta_encabezado = Label(text="Todos los Productos", font=('Calibri', 13))
        self.etiqueta_encabezado.grid(row=1, column=0, columnspan=2, sticky=W + E)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(self.ventana_a, height=20, columns=('#1', '#2', '#3', '#4', '#5', '#6', '#7'), style="mystyle.Treeview")
        self.tabla.grid(row=2, column=0, columnspan=2)
        self.tabla["show"] = "headings"
        self.tabla.heading("#1", text="Nombre", anchor=CENTER)
        self.tabla.heading("#2", text="Precio", anchor=CENTER)
        self.tabla.heading("#3", text="Categoria", anchor=CENTER)
        self.tabla.heading("#4", text="Stock", anchor=CENTER)
        self.tabla.heading('#5', text="Descripción", anchor=CENTER)
        self.tabla.heading('#6', text="Proveedor", anchor=CENTER)
        self.tabla.heading('#7', text="Ventas", anchor=CENTER)
        self.tabla.column('#7', width=100)
        self.tabla.column('#5', width=600)
        self.tabla.column('#4', width=100)
        self.tabla.column('#2', width=100)

        self.get_productos()

        self.etiqueta_encabezado2 = Label(text="Todos los Proveedores", font=('Calibri', 13))
        self.etiqueta_encabezado2.grid(row=3, column=0, columnspan=2, sticky=W + E)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla2 = ttk.Treeview(height=20, columns=('#1', '#2', '#3', '#4', '#5', '#6', '#7'),
                                  style="mystyle.Treeview")
        self.tabla2.grid(row=4, column=0, columnspan=2)
        self.tabla2["show"] = "headings"
        self.tabla2.heading("#1", text="Nombre Empresa", anchor=CENTER)
        self.tabla2.heading("#2", text="Telefono", anchor=CENTER)
        self.tabla2.heading("#3", text="Dirección", anchor=CENTER)
        self.tabla2.heading("#4", text="CIF", anchor=CENTER)
        self.tabla2.heading('#5', text="E-mail", anchor=CENTER)
        self.tabla2.heading('#6', text="Usuario", anchor=CENTER)
        self.tabla2.heading('#7', text="Contraseña", anchor=CENTER)


        self.boton_usuario = Button(text='Ventana Usuario', command= lambda :self.abrir_usuario())
        self.boton_usuario.grid(row=0, column=0, columnspan=2, sticky=W + E)

        self.get_proveedores()



    def dbp_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.dbp) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_proveedores(self):
        registros_tabla = self.tabla2.get_children()
        for fila in registros_tabla:
            self.tabla2.delete(fila)

        query = "SELECT * FROM proveedores"
        registros = self.dbp_consulta(query)

        for fila in registros:
            self.tabla2.insert("", 0, values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7]))


    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            self.tabla.insert("", 0, values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7]))

    def abrir_usuario(self):
        root = Tk()
        Ventas(root)
        root.mainloop()
