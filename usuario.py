from tkinter import ttk
from tkinter import *
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Voy a utilizar matplotlib para hacer la grafica
class Ventas:
    db = "database/producto.db"
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("El mercadillo de Sergio")
        self.ventana.resizable(0,0)
        self.ventana.configure(background="cyan")
        self.ventana.wm_iconbitmap("recursos/icon.ico")

        # El saldo inicial del usuario va a ser siempre 0, dejo luego un mensaje que dice que el saldo acaba en su tarjeta al finalizar el programa
        self.saldo = 0

        frame = LabelFrame(self.ventana, text="Gestion Usuario")
        frame.grid(row=0, column=0, rowspan=6)

        self.etiqueta_saldo = Label(frame, text="Su saldo es de: {} euros".format(self.saldo))
        self.etiqueta_saldo.grid(row=1, column=0)

        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 14, "bold"), background=('red'), foreground='green')

        boton_a_saldo = ttk.Button(frame, text="Añadir Saldo", style="my.TButton", command=lambda: self.aniadir_saldo())
        boton_a_saldo.grid(row=2, column=0, sticky=W + E)

        self.mensaje_d = Label(frame, text='''Se le devolvera todo el saldo a su 
        tarjeta cuando cierre el programa''', fg="orange")
        self.mensaje_d.grid(row=3, column=0)

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))

        boton_salir = ttk.Button(text="Salir", command=self.salir, style='my.TButton')
        boton_salir.grid(row=6, column=4, sticky=W + E)
        # La tabla con todos los productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        self.tabla = ttk.Treeview(self.ventana, height=20, columns=('#1', '#2', '#3', '#4', '#5'), style="mystyle.Treeview")
        self.tabla.grid(row=0, column=3, columnspan=2)
        self.tabla["show"] = "headings"
        self.tabla.heading("#1", text="Nombre", anchor=CENTER)
        self.tabla.heading("#2", text="Precio", anchor=CENTER)
        self.tabla.heading("#3", text="Categoria", anchor=CENTER)
        self.tabla.heading("#4", text="Stock", anchor=CENTER)
        self.tabla.heading("#5", text="Descripción", anchor=CENTER)
        self.tabla.column("#5", width=600)
        self.tabla.column("#4", width=100)
        self.tabla.column("#2", width=100)
        self.get_productos()

        boton_comprar = ttk.Button(text='COMPRAR', style="my.TButton", command=self.comprar)
        boton_comprar.grid(row=6, column=3, sticky=W + E)

        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=5, column=1, columnspan=4, sticky=W + E)
        # voy a crear la grafica frame2
        frame2 = Frame(self.ventana)
        frame2.grid(row=7, column=3)
        # Para la grafica necesitare datos y los sacare de la lista nombres y el otro de la lista ventas
        # De momento las dejo vacias
        nombres = []
        ventas = []
        query = "SELECT * FROM producto"
        resultados = self.db_consulta(query)
        for resultado in resultados:
            # Añado los nombres y ventas de los prodductos a las listas
            nombre = resultado[1]
            venta = resultado[7]
            nombres.append(nombre)
            ventas.append(venta)
        # Creo la grafica
        fig, axs = plt.subplots(dpi=80, figsize=(13, 4), sharey=True, facecolor='#00f9f844', constrained_layout=True)
        fig.suptitle('Grafica de Ventas')
        axs.bar(nombres, ventas)
        # Dibujo la grafica
        canvas = FigureCanvasTkAgg(fig, master=frame2)
        canvas.draw()
        canvas.get_tk_widget().grid(column=3, row=7, columnspan=4)

    # Estas dos funciones se repiten en los otros archivos y tienen el mismo funcionamiento
    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            print(fila)
            # Aqui no me ha dejado añadir nada a text, asi que lo he tenido que meter todo en values
            # Por lo tanto a partir de aqui he tenido que modificar toda la practica para que donde habia text ahora sera values [0]
            self.tabla.insert("", 0, values=(fila[1], fila[2], fila[3], fila[4], fila[5]))


    # Una funcion para salir directamente
    def salir(self):
        self.ventana.destroy()

    def comprar(self):
        global c
        global lista
        global lista_f
        # Intento seleccionar un producto
        try:
            precio = self.tabla.item(self.tabla.selection())['values'][1]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
            self.mensaje['text'] = ''

        # Si el saldo es menor al precio no se podrá comprar
        # Si el saldo es igual o mayor se comprará restando el precio al saldo y actualizando a menos 1 el stock
        # Si el saldo es igual o mayor pero no hay stock no se podra comprar
        stock = self.tabla.item(self.tabla.selection())['values'][3]
        if self.saldo >= precio and int(stock) > 0:
            self.mensaje['text'] = ''
            nombre = self.tabla.item(self.tabla.selection())['values'][0]
            query = '''UPDATE producto
                            SET stock=stock-1                            
                            WHERE nombre = ?'''  # Consulta SQL
            self.db_consulta(query, (nombre,))  # Ejecutar la consulta
            query2 = '''UPDATE producto
                            SET ventas=ventas+1
                            WHERE nombre = ?'''
            self.db_consulta(query2, (nombre,))
            self.mensaje['text'] = 'Producto {} comprado con éxito'.format(nombre)
            self.get_productos()  # Actualizar la tabla de productos
            self.saldo -= precio
            self.etiqueta_saldo["text"] = "Su saldo es de: {} euros".format(self.saldo)
        elif self.saldo >= precio and int(stock) == 0:
            nombre = self.tabla.item(self.tabla.selection())['values'][0]
            self.mensaje['text'] = 'No quedan unidades disponibles de {}'.format(nombre)
        elif self.saldo < precio:
            self.mensaje['text'] = 'Saldo insuficiente para comprar el producto'

    def aniadir_saldo(self):
        self.ventana_saldo = Toplevel(self.ventana)
        self.ventana_saldo.title = "El mercadillo de Sergio"
        self.ventana_saldo.configure(background='cyan')
        self.ventana_saldo.resizable(0, 0)
        self.ventana_saldo.wm_iconbitmap('recursos/icon.ico')
        frame_saldo = LabelFrame(self.ventana_saldo, text="Añadir saldo a su cuenta")
        frame_saldo.grid(row=0, column=0, columnspan=2)
        self.etiqueta_tarjeta = Label(frame_saldo, text="Introduzca el numero de su tarjeta")
        self.etiqueta_tarjeta.grid(row=1, column=0)
        self.tarjeta = Entry(frame_saldo)
        self.tarjeta.grid(row=1, column=1)
        self.etiqueta_intro_saldo = Label(frame_saldo, text="¿Cuanto saldo quiere añadir?")
        self.etiqueta_intro_saldo.grid(row=2, column=0)
        self.intro_saldo = Entry(frame_saldo)
        self.intro_saldo.grid(row=2, column=1)
        self.mensaje_s = Label(self.ventana_saldo, text="")
        self.mensaje_s.grid(row=4, column=0, columnspan=2)
        self.boton_saldo = Button(self.ventana_saldo, text="Hacer la operación", command=self.guardar_saldo)
        self.boton_saldo.grid(row=3, column=0, columnspan=2, sticky=W + E)

    def guardar_saldo(self):
        self.saldo += int(self.intro_saldo.get())
        self.mensaje_s["text"] = "Se han añadido {} euros a tu saldo".format(self.intro_saldo.get())
        self.intro_saldo.delete(0, END)
        self.tarjeta.delete(0, END)
        self.etiqueta_saldo["text"] = "Su saldo es de: {} euros".format(self.saldo)





