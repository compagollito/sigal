from datetime import datetime
from pymongo import MongoClient



class RegistroHistorico:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['historial_acceso']

    def registrar_acceso(self, correo, nombre, tipo, laboratorio):
        now = datetime.now()

        if tipo.lower() == "entrada":
            # Crear un registro nuevo de ingreso sin hora de salida
            registro = {
                "email": correo,
                "nombre_usuario": nombre,
                "hora_ingreso": now,
                "hora_salida": None,
                "laboratorio": laboratorio,
                "estado": "activo"
            }
            return self.collection.insert_one(registro).inserted_id

        elif tipo.lower() == "salida":
            # Actualizar el último registro activo del usuario
            filtro = {"email": correo, "hora_salida": None, "estado": "activo"}
            actualizacion = {
                "$set": {
                    "hora_salida": now,
                    "estado": "cerrado"
                }
            }
            resultado = self.collection.update_one(filtro, actualizacion)
            return resultado.modified_count

        else:
            raise ValueError("Tipo de registro debe ser 'Entrada' o 'Salida'.")
