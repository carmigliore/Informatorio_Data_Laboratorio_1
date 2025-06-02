import pandas as pd
from funciones.dataset import Dataset

class DatasetExcel(Dataset):
    def __init__(self, fuente_datos):
        super().__init__(fuente_datos)

    def cargar_datos(self):
        try:
            df = pd.read_excel(self.fuente_datos, engine='openpyxl')
            self.datos = df
            print("------")
            print(f"Datos cargados correctamente desde: {self.fuente_datos}")
            print("------")
            if self.validar_carga:
                self.transformar_datos()
        except Exception as e:
            raise ValueError(f"Error al cargar los datos desde el archivo Excel: {e}")
