import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from decouple import config

class GuardarDatos:
    def __init__(self):
        # Variables de entorno para la conexión a la base de datos
        user = config('DB_USER')
        password = config('DB_PASSWORD')
        host = config('DB_HOST')
        port = config('DB_PORT')
        self.database = config('DB_NAME')
            
        # Crea una ruta de conexión a la base de datos
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{self.database}"
        
        # Crea el motor de la base de datos y el self es para poder acceder a él desde def guardar_dataframe
        self.engine = create_engine(url)

    def guardar_dataframe(self, df, tabla):
        # Verifica si el DataFrame está vacío y el return corta el proceso si esta vacío
        if df.empty:
            print(f"El DataFrame está vacío. No se guardarán datos para la tabla:  {tabla}.")        
            return
        
        try:
            # Guarda el DataFrame en la tabla especificada y aunque exista la reemplaza
            # Si la tabla no existe, la crea automáticamente
            df.to_sql(tabla, con=self.engine, if_exists='replace', index=False)
            print(f"Datos guardados correctamente en BD: '{self.database}', tabla: '{tabla}'.")

        except SQLAlchemyError as e:
            print(f"Error al guardar la tabla: '{tabla}' en la base de datos: {e}")