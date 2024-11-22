import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from cliente import Cliente
from cliente_dao import ClienteDAO


class App(tk.Tk):
  COLOR_VENTANA = '#1d2d44'

  def __init__(self):
    super().__init__()
    self.id_cliente = None
    self.configurar_ventana()
    self.configurar_grid()
    self.mostrar_titulo()
    self.mostrar_formulario()
    self.cargar_tabla()
    self.mostrar_botones()

  def configurar_ventana(self):
    self.geometry('900x600')
    self.title('Zona Fit App')
    self.configure(background=App.COLOR_VENTANA)
    # Aplicamos el estilo
    self.estilos = ttk.Style()
    self.estilos.theme_use('clam')
    self.estilos.configure(self,
                           background=App.COLOR_VENTANA,
                           foreground='white',
                           fieldbackground='black')

  def configurar_grid(self):
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)

  def mostrar_titulo(self):
    etiqueta = ttk.Label(self, text='Zona Fit (GYM)',
                          font=('Arial', 30),
                          background=App.COLOR_VENTANA,
                          foreground='white')
    etiqueta.grid(row=0, column=0, columnspan=2, pady=30)

  def mostrar_formulario(self):
    self.frame_f = ttk.Frame()
    # Nombre
    nombre_l = ttk.Label(self.frame_f, text='Nombre:')
    nombre_l.grid(row=0, column=0, sticky=tk.W, pady=30, padx=5)
    self.nombre_t = ttk.Entry(self.frame_f)
    self.nombre_t.grid(row=0, column=1)
    # Apellido
    apellido_l = ttk.Label(self.frame_f, text='Apellido:')
    apellido_l.grid(row=1, column=0, sticky=tk.W, pady=30, padx=5)
    self.apellido_t = ttk.Entry(self.frame_f)
    self.apellido_t.grid(row=1, column=1)
    # Membresia
    membresia_l = ttk.Label(self.frame_f, text='Membresia:')
    membresia_l.grid(row=2, column=0, sticky=tk.W, pady=30, padx=5)
    self.membresia_t = ttk.Entry(self.frame_f)
    self.membresia_t.grid(row=2, column=1)


    # Publicamos el frame
    self.frame_f.grid(row=1, column=0)

  def cargar_tabla(self):
    # Creamos un frame para mostrar la tabla
    self.frame_tabla = ttk.Frame(self)
    # Definimos los estilos de la tabla
    self.estilos.configure('Treeview',
                           background='black',
                           foreground='white',
                           fieldbackground='black',
                           rowheight=30)
    columnas = ('Id', 'Nombre', 'Apellido', 'Membresia')
    # Cremaos el objeto tabla
    self.tabla = ttk.Treeview(self.frame_tabla,
                              columns=columnas,
                              show='headings')

    # agregar los cabeceros
    self.tabla.heading('Id', text='Id', anchor=tk.CENTER)
    self.tabla.heading('Nombre', text='Nombre', anchor=tk.W)
    self.tabla.heading('Apellido', text='Apellido', anchor=tk.W)
    self.tabla.heading('Membresia', text='Membresia', anchor=tk.W)

    # definimos las columnas
    self.tabla.column('Id', anchor=tk.CENTER, width=80)
    self.tabla.column('Nombre', anchor=tk.W, width=120)
    self.tabla.column('Apellido', anchor=tk.W, width=120)
    self.tabla.column('Membresia', anchor=tk.W, width=120)

    # Cargar los datos de la BD
    clientes = ClienteDAO.seleccionar()
    for c in clientes:
      self.tabla.insert(parent='',
                        index=tk.END,
                        values=(c.id, c.nombre, c.apellido, c.membresia))

    # agregar el scrollbar
    scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL,
                              command=self.tabla.yview)
    self.tabla.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky=tk.NS)

    # Mostramos la tabla
    self.tabla.grid(row=0, column=0)

    # Asociamos el evento select
    self.tabla.bind('<<TreeviewSelect>>', self.cargar_cliente)

    # Mostramos el frame
    self.frame_tabla.grid(row=1, column=1, padx=30)

  def mostrar_botones(self):
    self.frame_b = ttk.Frame()
    # Creamos los botones
    agregar_b = ttk.Button(self.frame_b, text='Guardar',
                           command=self.validar_cliente)
    agregar_b.grid(row=0, column=0, padx=30)
    eliminar_b = ttk.Button(self.frame_b, text='Eliminar',
                            command=self.eliminar_cliente)
    eliminar_b.grid(row=0, column=1, padx=30)
    limpiar_b = ttk.Button(self.frame_b, text='Limpiar',
                           command=self.limpiar_datos)
    limpiar_b.grid(row=0, column=2, padx=30)

    # Aplicamos un estilo a los botones
    self.estilos.configure('TButton', background='#005f73')
    self.estilos.map('TButton', background=[('active', '#0a9396')])

    # publicamos el frame
    self.frame_b.grid(row=2, column=0, columnspan=2, pady=40)

  def validar_cliente(self):
    # Validamos los campos
    if (self.nombre_t.get() and self.apellido_t.get()
      and self.membresia_t.get()):
      if self.validar_membresia():
        self.guardar_cliente()
      else:
        showerror(title='Atencion',
                  message='el valor de membresia NO es numerico')
        self.membresia_t.delete(0, tk.END)
        self.membresia_t.focus_set()
    else:
      showerror(title='Atencion', message='Debe llenar el formulario')
      self.nombre_t.focus_set()

  def validar_membresia(self):
    try:
      int(self.membresia_t.get())
      return True
    except:
      return False

  def guardar_cliente(self):
    # Recuperar los valores de las cajas de texto
    nombre = self.nombre_t.get()
    apellido = self.apellido_t.get()
    membresia = self.membresia_t.get()
    # Validamos el valor del self.id_cliente
    if self.id_cliente is None:  # Insertar
      cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
      ClienteDAO.insertar(cliente)
      showinfo(title='Agregar', message='Cliente agregado...')
    else:  # Actualizar
      cliente = Cliente(self.id_cliente, nombre, apellido, membresia)
      ClienteDAO.actualizar(cliente)
      showinfo(title='Actualizar', message='Cliente actualizado...')
    # Volvemos a mostrar los datos
    self.recargar_datos()

  def cargar_cliente(self, event):
    elemento_seleccionado = self.tabla.selection()[0]
    elemento = self.tabla.item(elemento_seleccionado)
    cliente_t = elemento['values']  # tupla con los valores
    # Recuperamos cada valor del cliente
    self.id_cliente = cliente_t[0]
    nombre = cliente_t[1]
    apellido = cliente_t[2]
    membresia = cliente_t[3]
    # Antes de cargar, limpiamos el formulario
    self.limpiar_formulario()
    # Cargar los valores en el formulario
    self.nombre_t.insert(0, nombre)
    self.apellido_t.insert(0, apellido)
    self.membresia_t.insert(0, membresia)

  def recargar_datos(self):
    # volvemos a cargar la tabla
    self.cargar_tabla()
    # limpiamos datos
    self.limpiar_datos()

  def limpiar_datos(self):
    self.limpiar_formulario()
    self.id_cliente = None

  def limpiar_formulario(self):
    self.nombre_t.delete(0, tk.END)
    self.apellido_t.delete(0, tk.END)
    self.membresia_t.delete(0, tk.END)

  def eliminar_cliente(self):
    if self.id_cliente is None:
      showerror(title='Antencion',
                message='Debe seleccionar un cliente a eliminar')
    else:
      cliente = Cliente(id=self.id_cliente)
      ClienteDAO.eliminar(cliente)
      showinfo(title='Eliminado', message='Cliente eliminado...')
      self.recargar_datos()


if __name__ == '__main__':
  app = App()
  app.mainloop()