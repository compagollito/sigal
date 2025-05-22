import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

class HistorialAccesoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Historial de Accesos")
        self.geometry("900x500")
        self.configure(bg="#F5F5F5")

        # Cargar variables y conectar
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        mongo_name = os.getenv("MONGO_NAME")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[mongo_name]
        self.collection = self.db['historial_acceso']
        
        # Obtener laboratorios desde MongoDB
        laboratorios = [lab.get("nombre") for lab in self.db.laboratorys.find()]
        laboratorios.sort()  # Opcional: ordenar alfabéticamente
        laboratorios.insert(0, "Todos")  # Insertar opción "Todos" al inicio

        self.laboratorios = laboratorios

        self.create_widgets()
        self.cargar_registros()

    def create_widgets(self):
        # Filtro laboratorio
        filtro_frame = tk.Frame(self, bg="#F5F5F5")
        filtro_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(filtro_frame, text="Filtrar por laboratorio:", bg="#F5F5F5", font=("Arial", 12)).pack(side=tk.LEFT)

        self.combo_lab = ttk.Combobox(filtro_frame, values=self.laboratorios, state="readonly", width=20)
        self.combo_lab.current(0)
        self.combo_lab.pack(side=tk.LEFT, padx=10)

        btn_filtrar = tk.Button(filtro_frame, text="Aplicar filtro", command=self.cargar_registros)
        btn_filtrar.pack(side=tk.LEFT)

        # Treeview para mostrar registros
        columnas = ("email", "nombre_usuario", "tipo", "laboratorio", "hora_ingreso", "hora_salida", "estado")
        self.tree = ttk.Treeview(self, columns=columnas, show='headings')
        for col in columnas:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor=tk.CENTER)
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def cargar_registros(self):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        filtro_lab = self.combo_lab.get()
        query = {}
        if filtro_lab != "Todos":
            query["laboratorio"] = filtro_lab

        registros = self.collection.find(query).sort("hora_ingreso", -1)

        for reg in registros:
            # Obtener tipo (entrada o salida)
            tipo = "Entrada" if reg.get("hora_salida") is None else "Salida"

            # Formatear fechas
            hora_ingreso = reg.get("hora_ingreso")
            if isinstance(hora_ingreso, datetime):
                hora_ingreso = hora_ingreso.strftime("%d/%m/%Y %H:%M:%S")
            hora_salida = reg.get("hora_salida")
            if isinstance(hora_salida, datetime):
                hora_salida = hora_salida.strftime("%d/%m/%Y %H:%M:%S")
            else:
                hora_salida = "-"

            self.tree.insert("", "end", values=(
                reg.get("email", ""),
                reg.get("nombre_usuario", ""),
                tipo,
                reg.get("laboratorio", ""),
                hora_ingreso,
                hora_salida,
                reg.get("estado", "")
            ))

if __name__ == "__main__":
    app = HistorialAccesoApp()
    app.mainloop()
