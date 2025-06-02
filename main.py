from os import path
from funciones.dataset_csv import DatasetCSV
from funciones.dataset_excel import DatasetExcel
from guardar_bd.guardar_datos import GuardarDatos

# Ruta de archivos
csv_1_path = path.join(path.dirname(__file__), "archivos/bienes-secuestrados-2025.csv")
csv_2_path = path.join(path.dirname(__file__), "archivos/crop_recommendation.csv")
excel_path = path.join(path.dirname(__file__), "archivos/ListaTramitesAT21112024.xlsx")

# Cargar y transformar (lee dataset_csv.py y dataset_excel.py de la carpeta funciones)
csv_1 = DatasetCSV(csv_1_path)
csv_1.cargar_datos()
csv_1.mostrar_resumen()

csv_2 = DatasetCSV(csv_2_path)
csv_2.cargar_datos()
csv_2.mostrar_resumen()

excel = DatasetExcel(excel_path)
excel.cargar_datos()
excel.mostrar_resumen()

# Guardar en base de datos (lee de guardar_datos.py)
db = GuardarDatos()
db.guardar_dataframe(csv_1.datos, "bienes_secuestrados_2025_csv_2")
db.guardar_dataframe(csv_2.datos, "crop_recommendation_csv")
db.guardar_dataframe(excel.datos, "lista_tramites_at_211124_excel")