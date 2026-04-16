import json
import os
from myLogs import logger

class JsonDB:
    def __init__(self, path, default=None):
        self.path = path
        self.default = default if default is not None else {}
        logger.info(f"Iniciando JsonDB para {self.path}")
        self.data = self._load()

    def _ensure_exists(self):
        if not os.path.exists(self.path):
            logger.warning(f"Archivo {self.path} no existe. Creando nuevo archivo.")
            with open(self.path, "w") as f:
                json.dump(self.default, f, indent=4)
            logger.info(f"Archivo {self.path} creado con default={self.default}")

    def _load(self):
        self._ensure_exists()
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                logger.info(f"Archivo {self.path} cargado correctamente.")
                return data
        except json.JSONDecodeError:
            logger.error(f"Error al leer {self.path}. JSON corrupto. Restaurando default.")
            self.data = self.default  # ← FIX
            self.save()
            return self.data

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)
        logger.info(f"Datos guardados en {self.path}")

    # -------------------------
    # Métodos para diccionarios
    # -------------------------
    def set(self, key, value):
        if not isinstance(self.data, dict):
            logger.error("Intento de usar set() en un JSON que no es diccionario.")
            raise TypeError("Este JSON no es un diccionario")

        self.data[key] = value
        logger.info(f"Set: {key} = {value} en {self.path}")
        self.save()

    def get(self, key, default=None):
        if not isinstance(self.data, dict):
            logger.error("Intento de usar get() en un JSON que no es diccionario.")
            raise TypeError("Este JSON no es un diccionario")

        return self.data.get(key, default)

    def exists(self, key):
        if not isinstance(self.data, dict):
            logger.error("Intento de usar exists() en un JSON que no es diccionario.")
            raise TypeError("Este JSON no es un diccionario")

        existe = key in self.data
        logger.info(f"Exists: {key} -> {existe}")
        return existe

    # -------------------------
    # Métodos para listas
    # -------------------------
    def append(self, item):
        if not isinstance(self.data, list):
            logger.error("Intento de usar append() en un JSON que no es lista.")
            raise TypeError("Este JSON no es una lista")
        
        # Comprobar duplicados
        tiene_fecha_y_estacion = "Fecha" in item and "Estacion" in item

        if tiene_fecha_y_estacion:
            for registro in self.data:
                if (registro.get("Fecha") == item.get("Fecha") and
                    registro.get("Estacion") == item.get("Estacion")):
                    
                    logger.warning(
                        f"Registro duplicado detectado en {self.path}: "
                        f"Fecha={item.get('Fecha')}, Estacion={item.get('Estacion')}"
                    )
                    print("Registro duplicado, no se guarda")
                    return None
            
        # Generar ID autoincremental
        if len(self.data) == 0:
            new_id = 1
        else:
            ids = [r.get("id", 0) for r in self.data]
            new_id = max(ids) + 1

        # Crear el registro con ID incluido
        item_with_id = {"id": new_id, **item}

        self.data.append(item_with_id)
        logger.info(f"Append: id: {new_id}, añadido {item} a {self.path} con")
        print("Registro añadido correctamente.")
        logger.info(f"Nuevo registro añadido: {item_with_id}")
        self.save()

        return new_id

    def extend(self, items):
        if not isinstance(self.data, list):
            logger.error("Intento de usar extend() en un JSON que no es lista.")
            raise TypeError("Este JSON no es una lista")

        self.data.extend(items)
        logger.info(f"Extend: añadidos {len(items)} elementos a {self.path}")
        self.save()
    
    def delete(self, key):
        if not isinstance(self.data, dict):
            logger.error("Intento de usar delete() en un JSON que no es diccionario.")
            raise TypeError("Este JSON no es un diccionario")

        if key not in self.data:
            logger.info(f"Delete: {key} no existe en {self.path}")
            return False

        del self.data[key]
        logger.info(f"Delete: {key} eliminado de {self.path}")
        self.save()
        return True
