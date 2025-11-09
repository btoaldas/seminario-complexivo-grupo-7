import pandas as pd
import os

# Creación de función
def cargar_datos_excel(path, lista_de_hojas):
    print(f"Cargando datos desde {path}...")

    dataframe_cargados = {}

    try:
        for hoja in lista_de_hojas:
            print(f"Leyendo hoja: {hoja} ...")
            df_temporal = pd.read_excel(path, sheet_name=hoja)
            dataframe_cargados[hoja] = df_temporal

        print("Datos han sido cargados!!!")
        return dataframe_cargados

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo en {path}")
        print("Asegúrate de tener el archivo en la carpeta 'data'.")
        return None

    except Exception as e:
        print(f"Ocurrió un error inesperado {e}")
        return None