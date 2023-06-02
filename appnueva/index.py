from tkinter import ttk
from tkinter import *
import sqlite3

from mysqlx import Row
# Nombre del cliente / diré/ CEL/productos / precio/ total


class Produc:
    db_name = "database.db"

    def __init__(self, window):
        self.ventana = window
        self.ventana.title("Estefy Natura")

        # contenedor
        Frame = LabelFrame(self.ventana, text='Clientes')
        Frame.grid(row=0, column=0, columnspan=3, pady=20)

        # entrada nombre
        Label(Frame, text="Producto ").grid(row=1, column=0)
        self.nombre = Entry(Frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        # Entrada precio
        Label(Frame, text="Precio").grid(row=2, column=0)
        self.precio = Entry(Frame)
        self.precio.grid(row=2, column=1)

        # botones
        ttk.Button(Frame, text="Guardar Todo", command=self.add_productos).grid(
            row=3, columnspan=2, sticky=W + E)

        # Tabla
        self.tabla = ttk.Treeview(height=10, columns=2)
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla.heading("#1", text="Precio", anchor=CENTER)

        self.get_products()

    def run_query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
            return resultado

    def get_products(self):
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
# Consulta
        query = "select * from productos order by nombre desc"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tabla.insert("", 0, text=row[1], values=row[2])

    def validacion(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0

# entrada de productos

    def add_productos(self):
        if self.validacion():
            query = "INSERT INTO productos VALUES (NULL,?,?)"
            parametro = (self.nombre.get(), self.precio.get())
            self.run_query(query, parametro)
            print("Carga completa ")
        else:
            print("nombre y precio requerido")
        self.get_products()


if __name__ == "__main__":
    window = Tk()
    applicacion = Produc(window)
    window.mainloop()
