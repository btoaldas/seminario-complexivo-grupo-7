import pandas as pd
import os

# Ruta absoluta de la carpeta donde se encuentra este script (.../scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta del archivo xlsx en la carpeta data
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data", "dataset.xlsx")

# Creación de la función para cargar los datos
def cargar_datos(path):
   print(f"Cargando datos desde: {path}")
   try:
       df = pd.read_excel(path)
       print("Datos cargados exitosamente.")
       return df
   except FileNotFoundError:
       print("Error: El archivo no se encontró.")
       print("Verifique que la ruta sea correcta y que el archivo exista en 'data'.")
   except Exception as e:
       print(f"Error al cargar los datos: {e}")
       return None

#¿Este archivo se está ejecutando directamente por el usuario o esta siendo importado por otro script?
if __name__ == "__main__":
    # indica donde está el script actual
    print(f"Directorio del script: {os.path.abspath(__file__)}")
    
    # llama a la funcion de arriba para cargar los datos
    dataframe_fifa = cargar_datos(DATA_PATH)
    if dataframe_fifa is not None:
        print("\n -- Primeras filas del DataFrame --")
        print(dataframe_fifa.head())
        print("\n -- Información del DataFrame --")
        print(dataframe_fifa.info())
        