# %%
import pandas as pd
import numpy as np
import os


def union_dataframes(dataframes): 
    
    try: 
        df_pedidos = dataframes["Orders"]
        df_devoluciones = dataframes["Returns"]
        df_personas = dataframes["People"]
        
        print("Se está uniendo archivo Pedidos con Devoluciones...")
        df_maestro = pd.merge(
            left = df_pedidos, 
            right = df_devoluciones, 
            on = "Order ID", 
            how = "left"
        )
        
        df_maestro["Returned"] = df_maestro["Returned"].fillna("No")
        
        print("Listo. Ahora se está uniendo archivo Maestro con Personas...")
        
        df_maestro = pd.merge(
            left = df_maestro, 
            right = df_personas, 
            on = "Region", 
            how = "left"
        )
        
        print("Unión lista!!!")
        
        return df_maestro
    
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        
        

def guardar_datos_procesados(df, path):
    """
    guarda DataFrame final en nueva ruta
    """
    try:
        # intenta crear esta carpeta, si existe, no hagas nada
        # os.path.dirname(path): esta función "corta" el string de la ruta y devuelve solo el nombre del directorio (la carpeta) que lo contiene resultado: "data/processed"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # convertir el archivo en csv, no guardamos el índice
        df.to_csv(path, index=False)
        print(f"Datos consolidados guardados exitosamente en: {path}")
        return True # retorna True si tuvo éxito
        
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False # retorna False si falló