from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    db = "database/producto.db"
    dbp = "database/proveedores.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("El mercadillo de Sergio")
        self.ventana.resizable(0,0)
        self.ventana.configure(background="cyan")
        self.ventana.wm_iconbitmap("recursos/icon.ico")

        # Creacion del Frame pincipal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=4, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0)

        # Entry Precio
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        # Label categoria
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=3, column=0)

        # Entry categoria
        self.categoria = Entry(frame, font=('Calibri', 13))
        self.categoria.grid(row=3, column=1)

        # Label stock
        self.etiqueta_stock = Label(frame, text="Stock: ", font=('Calibri', 13))
        self.etiqueta_stock.grid(row=4, column=0)

        # Entry stock
        self.stock = Entry(frame, font=('Calibri', 13))
        self.stock.grid(row=4, column=1)

        # Label descripcion
        self.etiqueta_descripcion = Label(frame, text="Descripción: ", font=('Calibri', 13))
        self.etiqueta_descripcion.grid(row=5, column=0)

        # Entry descripcion
        self.descripcion = Entry(frame, font=('Calibri', 13))
        self.descripcion.grid(row=5, column=1)

        # Boton de Añadir Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))

        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=6, columnspan=2, sticky=W + E)

        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=6, column=0, columnspan=2, sticky=W + E)

        self.etiqueta_encabezado = Label(text="Mis Productos en Venta", font=('Calibri', 13))
        self.etiqueta_encabezado.grid(row=8, column=0, columnspan=2, sticky=W + E)

        # Tabla Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=('#1', '#2', '#3', '#4', '#5', '#6'), style="mystyle.Treeview")
        self.tabla.grid(row=9, column=0, columnspan=2)
        self.tabla["show"] = "headings"
        self.tabla.heading("#1", text="Nombre", anchor=CENTER)
        self.tabla.heading("#2", text="Precio", anchor=CENTER)
        self.tabla.heading("#3", text="Categoria", anchor=CENTER)
        self.tabla.heading("#4", text="Stock", anchor=CENTER)
        self.tabla.heading('#5', text="Descripción", anchor=CENTER)
        self.tabla.heading('#6', text="Ventas", anchor=CENTER)
        self.tabla.column('#6', width=100)
        self.tabla.column('#5', width=600)
        self.tabla.column('#4', width=100)
        self.tabla.column('#2', width=100)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 14, "bold"), background=('red'), foreground='green')

        boton_eliminar = ttk.Button(text='ELIMINAR', style="my.TButton", command=self.del_producto)
        boton_eliminar.grid(row=10, column=0, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', style="my.TButton", command=self.edit_producto)
        boton_editar.grid(row=10, column=1, sticky=W + E)

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado



    def get_productos(self):
        # Borramos los datos antiguos de la tabla

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        # Aqui voy a hacer la consulta SQL para que seleccione el nombre de la empresa del usuario que se ha logeado

        from main import usuario_p
        query = "SELECT nombre_empresa FROM proveedores WHERE usuario = (?)"
        conexion = sqlite3.connect('database/proveedores.db')
        cursor = conexion.cursor()
        cursor.execute(query, (usuario_p,))
        datos = cursor.fetchall()
        for dato in datos:
            nombre_empresa = dato[0]
        conexion.close()
        # Ahora que tengo el nombre de la empresa saco los productos que tiene esa empresa, asi el usuario solo vera sus productos
        query = "SELECT * FROM producto WHERE nombre_empresa = (?)"
        registros = self.db_consulta(query, (nombre_empresa,))

        for fila in registros:
            print(fila)
            # Aqui me salto de mostrar el nombre de la empresa y voy a añadir la fila[7] que es las ventas
            self.tabla.insert("", 0, values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[7]))
            # En vez de hacerlo en porcentajes he decidido hacer que si hay 3 o menos de stock mande el mensaje de queda poco
            if fila[4] <= 3 and fila[4] > 0:
                self.mensaje["text"] = "Te queda poco stock de {}".format(fila[1])
            # Si hay 0 dira que no queda stock
            elif fila[4] == 0:
                self.mensaje["text"] = "No te queda nada de stock del producto {}".format(fila[1])
    # Validaciones para que no dejen campos sin rellenar
    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducida_por_usuario = self.categoria.get()
        return len(categoria_introducida_por_usuario) != 0

    def validacion_stock(self):
        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0
    def validacion_descripcion(self):
        descripcion_introducida_por_usuario = self.descripcion.get()
        return len(descripcion_introducida_por_usuario) != 0


    def add_producto(self):
        from main import usuario_p
        # Aqui la idea es automatizar que cada producto que se agregue registre automaticamente el nombre de la empresa del usuario
        # En principio como se acaba de registrar el producto sus ventas seran 0
        ventas = 0
        query = "SELECT nombre_empresa FROM proveedores WHERE usuario = (?)"
        conexion = sqlite3.connect('database/proveedores.db')
        cursor = conexion.cursor()
        cursor.execute(query, (usuario_p,))
        datos = cursor.fetchall()
        for dato in datos:
            nombre_empresa = dato[0]
        conexion.close()
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_stock() and self.validacion_categoria() and self.validacion_descripcion():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get(), self.descripcion.get(), nombre_empresa, ventas)
            self.db_consulta(query, parametros)
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END)  # Borrar el campo precio del formulario
            self.categoria.delete(0, END)  # Borrar el campo categoria del formulario
            self.stock.delete(0, END)  # Borrar el campo stock del formulario
            self.descripcion.delete(0, END)


        elif self.validacion_nombre() or self.validacion_precio() or self.validacion_categoria() or self.validacion_stock() or self.validacion_descripcion() == False:
            print("Algun campo ha quedado vacio")
            self.mensaje["text"] = "Rellene todos los campos"

        else:
            print("Introduzca bien los datos")
            self.mensaje["text"] = "Error de datos"

        self.get_productos()

    def del_producto(self):
        # Esta parte del código es la misma que en la practica del modulo 6

        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['values'][0]
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['values'][0]
        old_precio = self.tabla.item(self.tabla.selection())['values'][1]
        old_categoria = self.tabla.item(self.tabla.selection())['values'][2]
        old_stock = self.tabla.item(self.tabla.selection())['values'][3]
        old_descripcion = self.tabla.item(self.tabla.selection())['values'][4]
        self.ventana_editar = Toplevel()
        self.ventana_editar.title = "Editar Producto"
        self.ventana_editar.configure(background='cyan')
        self.ventana_editar.resizable(0, 0)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)


        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto",
                              font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ",
                                             font=('Calibri', 13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
                                          state='readonly', font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ",
                                             font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_antiguo.grid(row=4, column=0)  # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly', font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoria antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13))
        self.etiqueta_categoria_antigua.grid(row=6, column=0)
        # Entry Categoria antigua
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                             state='readonly', font=('Calibri', 13))
        self.input_categoria_antigua.grid(row=6, column=1)

        # Label categoria nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoria nueva", font=('Calibri', 13))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)
        # Entry categoria nueva
        self.input_categoria_nueva = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nueva.grid(row=7, column=1)

        # Label stock antiguo
        self.etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo", font=('Calibri', 13))
        self.etiqueta_stock_antiguo.grid(row=8, column=0)
        # Entry stock antiguo
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                         state='readonly', font=('Calibri', 13))
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo", font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        # Entry stock nuevo
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=9, column=1)

        # Label y Entry descripcion antigua
        self.etiqueta_descripcion_antigua = Label(frame_ep, text="Descripción antigua", font=('Calibri', 13))
        self.etiqueta_descripcion_antigua.grid(row=10, column=0)
        self.input_descripcion_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_descripcion),
                                         state='readonly', font=('Calibri', 13))
        self.input_descripcion_antigua.grid(row=10, column=1)

        # Label y Entry descripcion nueva
        self.etiqueta_descripcion_nueva = Label(frame_ep, text="Descripción nueva", font=('Calibri', 13))
        self.etiqueta_descripcion_nueva.grid(row=11, column=0)
        self.input_descripcion_nueva = Entry(frame_ep, font=('Calibri', 13))
        self.input_descripcion_nueva.grid(row=11, column=1)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 14, "bold"))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style="my.TButton",
                                           command=lambda:
                                           self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                     self.input_nombre_antiguo.get(),
                                                                     self.input_precio_nuevo.get(),
                                                                     self.input_precio_antiguo.get(),
                                                                     self.input_categoria_nueva.get(),
                                                                     self.input_categoria_antigua.get(),
                                                                     self.input_stock_nuevo.get(),
                                                                     self.input_stock_antiguo.get(),
                                                                     self.input_descripcion_nueva.get(),
                                                                     self.input_descripcion_antigua.get()))
        self.boton_actualizar.grid(row=12, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria,
                             antigua_categoria, nuevo_stock, antiguo_stock, nueva_descripcion, antigua_descripcion):
        # los campos de nombre_empresa y ventas no dejaremos que los modifiquen
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ?, descripcion = ? WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ? AND descripcion = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '' and nueva_descripcion != '':
            # Si el usuario escribe nuevo nombre, nuevo precio, nueva categoria, nuevo stock y nueva descripcion se cambia todo
            parametros = (
            nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, nueva_descripcion, antiguo_nombre, antiguo_precio, antigua_categoria,
            antiguo_stock, antigua_descripcion)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '' and nueva_categoria != '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, nueva_descripcion, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock, antigua_descripcion)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '' and nueva_descripcion != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, nueva_descripcion, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock, antigua_descripcion)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '' and nueva_descripcion != '':
            # Cambia todo menos la categoria
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, nueva_categoria, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '' and nueva_descripcion != '':
            # Cambia todo menos el stock
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, nueva_categoria, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '' and nueva_descripcion == '':
            # Solo cambio el precio
            parametros = (
            antiguo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antigua_descripcion, antiguo_nombre, antiguo_precio,
            antigua_categoria, antiguo_stock, antigua_descripcion)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '' and nueva_descripcion == '':
            parametros = (
                antiguo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antigua_descripcion, antiguo_nombre, antiguo_precio,
                antigua_categoria, antiguo_stock, antigua_descripcion)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '' and nueva_descripcion == '':
            # Cambio de precio y de stock, que es un cambio habitual
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antigua_descripcion, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock, antigua_descripcion)
            producto_modificado = True

        # En caso de que se escoja una combinacion que no tengo saldra el mensaje del else del siguiente condicional
        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(
                antiguo_nombre)  # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(
                antiguo_nombre)  # Mostrar mensaje para el usuario


