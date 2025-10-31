import pandas as pd
import os

def gaurdar_datos_limpios(df, path):
    """
    guarda el DataFrame limpio en un archivo CSV.
    
    args:
        df: DataFrame a guardar
        path: ruta donde se guardará el archivo CSV
    """
    try:
        print(f"guardando DataFrame limpio en: {path}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        
        print("DataFrame guardado exitosamente.")
        print(f"{path})
        return True
        
        