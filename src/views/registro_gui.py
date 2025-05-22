import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from registro_historial import RegistroHistorico
from historial_gui import HistorialAccesoApp
import os

class RegistroAccesoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIGAL - Registro de Acceso")
        self.geometry("850x250")
        self.configure(bg="#F5F5F5")

        # Conexión a MongoDB
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.mongo_name = os.getenv("MONGO_NAME")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_name]
        self.usuarios = self.db.users  # Asegúrate que esta es la colección correcta
        self.registro_historico = RegistroHistorico(self.mongo_uri, self.mongo_name)
        self.create_widgets()

    def create_widgets(self):
        # Barra superior
        barra = tk.Frame(self, bg="#F5F5F5", height=50)
        barra.pack(fill=tk.X)

        titulo = tk.Label(barra, text="SIGAL", font=("Arial", 16, "bold"), bg="#F5F5F5")
        titulo.pack(side=tk.LEFT, padx=10, pady=10)

        icono_usuario = tk.Label(barra, text="👤", font=("Arial", 16), bg="#F5F5F5")
        icono_usuario.pack(side=tk.RIGHT, padx=10)

        # Sección ingreso datos y selección
        frame_ingreso = tk.LabelFrame(self, text="Registrar Acceso", font=("Arial", 12, "bold"), bg="#F5F5F5")
        frame_ingreso.pack(fill=tk.X, padx=20, pady=10)

        # Correo
        lbl_correo = tk.Label(frame_ingreso, text="Correo:", bg="#F5F5F5", font=("Arial", 11))
        lbl_correo.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.entry_correo = tk.Entry(frame_ingreso, font=("Arial", 11), width=30)
        self.entry_correo.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Contraseña
        lbl_contra = tk.Label(frame_ingreso, text="Contraseña:", bg="#F5F5F5", font=("Arial", 11))
        lbl_contra.grid(row=0, column=2, padx=5, pady=10, sticky="w")
        self.entry_contra = tk.Entry(frame_ingreso, font=("Arial", 11), show="*", width=20)
        self.entry_contra.grid(row=0, column=3, padx=5, pady=10, sticky="w")

        # Tipo de registro
        lbl_tipo = tk.Label(frame_ingreso, text="Tipo de Registro:", bg="#F5F5F5", font=("Arial", 11))
        lbl_tipo.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.tipo_registro = ttk.Combobox(frame_ingreso, values=["Entrada", "Salida"], state="readonly", font=("Arial", 11), width=10)
        self.tipo_registro.current(0)
        self.tipo_registro.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Laboratorio
        lbl_lab = tk.Label(frame_ingreso, text="Laboratorio:", bg="#F5F5F5", font=("Arial", 11))
        lbl_lab.grid(row=1, column=2, padx=5, pady=10, sticky="w")
        #self.combo_lab = ttk.Combobox(frame_ingreso, values=["Laboratorio 1", "Laboratorio 2", "Laboratorio 3"], state="readonly", font=("Arial", 11), width=20)
        laboratorios = [lab.get("nombre") for lab in self.db.laboratorys.find()]

        # Crear Combobox con valores dinámicos
        self.combo_lab = ttk.Combobox(frame_ingreso, values=laboratorios, state="readonly", font=("Arial", 11), width=20)
        
        
        self.combo_lab.current(0)
        self.combo_lab.grid(row=1, column=3, padx=5, pady=10, sticky="w")

        # Botón Registrar
        btn_registrar = tk.Button(frame_ingreso, text="Registrar", command=self.registrar, bg="#4CAF50", fg="white", font=("Arial", 11))
        btn_registrar.grid(row=1, column=4, padx=10, pady=10)
        
        btn_ver_historial = tk.Button(barra, text="Ver Historial", command=self.abrir_historial, bg="#2196F3", fg="white", font=("Arial", 11))
        btn_ver_historial.pack(side=tk.RIGHT, padx=10)

    def abrir_historial(self):
        ventana_historial = HistorialAccesoApp()
        ventana_historial.grab_set()
    
    def registrar(self):
        correo = self.entry_correo.get().strip()
        contra = self.entry_contra.get().strip()
        tipo = self.tipo_registro.get()
        laboratorio = self.combo_lab.get()

        if not correo or not contra:
            messagebox.showwarning("Aviso", "Por favor, ingresa correo y contraseña.")
            return

        nombre = self.buscar_nombre_usuario(correo, contra)
        if nombre == "Usuario Desconocido":
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")
            return

         # Guardar el registro histórico
        registros_guardados = self.registro_historico.registrar_acceso(correo, nombre, tipo, laboratorio)
        #self.registro_historico = RegistroHistorico(self.mongo_uri, self.mongo_name)

        if tipo.lower() == "entrada":
            msg = f"Entrada registrada para {nombre} a las {datetime.now().strftime('%H:%M:%S')}"
        else:
            if registros_guardados == 0:
                messagebox.showwarning("Aviso", "No se encontró registro abierto para cerrar la salida.")
                return
            msg = f"Salida registrada para {nombre} a las {datetime.now().strftime('%H:%M:%S')}"

        messagebox.showinfo("Registro", msg)

        # Limpiar entradas
        self.entry_correo.delete(0, tk.END)
        self.entry_contra.delete(0, tk.END)

    def buscar_nombre_usuario(self, correo, contra):
        usuario = self.usuarios.find_one({"email": correo, "password": contra})
        if usuario:
            # Unimos los campos para mostrar el nombre completo
            nombre_completo = f"{usuario.get('first_name', '')} {usuario.get('middle_name', '')} {usuario.get('last_name', '')}"
            return nombre_completo.strip()
        else:
            return "Usuario Desconocido"


if __name__ == "__main__":
    app = RegistroAccesoApp()
    app.mainloop()
