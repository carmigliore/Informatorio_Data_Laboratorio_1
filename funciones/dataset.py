from abc import ABC, abstractmethod
import pandas as pd
import unicodedata

class Dataset(ABC):
    def __init__(self, fuente_datos):
    # Encapsula la fuente de datos y los datos para que no se puedan modificar directamente
        self.__fuente_datos = fuente_datos
        self.__datos = None
    
    # Decorador de python para que "datos" se pueda leer 
    @property  
    def datos(self):
        return self.__datos
    
    # Decorador de python para que "datos" se pueda escribir
    @datos.setter  
    def datos(self, value):
        if not isinstance(value, pd.DataFrame):
            raise TypeError("El valor debe ser un DataFrame de pandas.")
        self.__datos = value
    
    @property
    def fuente_datos(self):
        return self.__fuente_datos  
    
    @abstractmethod
    def cargar_datos(self):
        # Es obligatorio implementarlo en la herencia y generico para que las subclases lo modifiquen
        pass

    def validar_carga(self):
        # Verifica si los datos están cargados de lo contrario corta el proceso
        if self.datos is None:
            raise ValueError("Los datos no han sido cargados. Por favor, carga los datos primero.")

    def transformar_datos(self):
        if self.datos is not None:        
            # Normaliza nombres de columna: Los convierte en minúsculas, reemplaza espacios internos por "_" y quita acentos
            self.__datos.columns = [
                unicodedata.normalize('NFKD', col).encode('ascii', 'ignore').decode('utf-8')
                for col in self.datos.columns.str.lower().str.replace(" ", "_")
                ]
            print("Los nombres de las columnas han sido normalizados.")

            # Elimina filas completamente vacías y muestra mensaje si se eliminaron
            filas_antes = len(self.datos)
            self.datos = self.datos.dropna(how="all")
            filas_despues = len(self.datos)
            if filas_antes > filas_despues:
                print(f"Se eliminaron {filas_antes - filas_despues} filas completamente vacías.")
            else:
                print("No se encontraron filas completamente vacías para eliminar.")

            # Reemplaza celdas vacías por el texto "null"
            celdas_vacias = self.datos.isnull().sum().sum()
            if celdas_vacias > 0:
                print(f"Advertencia: Se encontraron {celdas_vacias} celdas vacías. Se reemplazarán por 'null'.")
                self.__datos = self.datos.fillna("null")
            else:
                print("No se encontraron celdas vacías para reemplazar.")

            # Convierte todos los registros de tipo texto a tipo string, borra espacios al inicio y final pero mantiene el tipo original de los datos fecha            
            for col in self.datos.select_dtypes(include="object").columns:
                self.__datos[col] = self.datos[col].astype(str).str.strip()
            print("Todos los datos (salvo fecha y moneda) han sido convertidos a tipo string y removidos los espacios en blanco inicial y final.")

            '''# Elimina filas duplicadas
            duplicados = self.datos.duplicated().sum()
            if duplicados > 0:
                print(f"Advertencia: Se eliminaron {duplicados} filas duplicadas.")
                self.__datos = self.datos.drop_duplicates()
            else:
                print("No se encontraron filas duplicadas para eliminar.")'''

            # Marca filas duplicadas en una nueva columna
            self.__datos["duplicada"] = self.datos.duplicated().replace({True: "duplicada", False: ""})
            duplicados = (self.__datos["duplicada"] == "duplicada").sum()
            if duplicados > 0:
                print(f"Advertencia: Se identificaron {duplicados} filas duplicadas en la columna 'duplicada'.")
            else:
                print("No se encontraron filas duplicadas para identificar.")

    def mostrar_resumen(self):
        if self.datos is not None:
            print("Resumen del DataFrame:")
            print(self.datos.describe(include='all')) 
            print(self.datos.info())
        else:
            print("No hay datos cargados para mostrar el resumen.")