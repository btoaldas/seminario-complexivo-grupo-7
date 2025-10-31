import pandas as pd
import os

def guardar_datos_limpios(df, path):
    """
    guarda el DataFrame final procesado como archivo CSV.
    crea la carpeta de destino automaticamente si no existe.
    
    parámetros:
        df: DataFrame limpio y procesado listo para guardar
        path: ruta completa donde se guardara el archivo CSV
        
    retorna:
        True si se guardo correctamente, False si hubo error
    """
    try:
        print("Guardando datos limpios...")
        
        # crear carpeta 'processed' si no existe
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # guardar como CSV sin indices
        df.to_csv(path, index=False)
        
        print("\nArchivo guardado exitosamente en:")
        print(f"{path}")
        
        return True
    
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        
        return False
