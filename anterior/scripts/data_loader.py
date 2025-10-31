# archivo: data_loader.py
# -*- coding: utf-8 -*-
"""
cargador de datos fifa - lee el archivo excel con todas las hojas
proporciona funciones para cargar el dataset completo o hojas individuales
"""

import pandas as pd
import os
from typing import Dict, Optional

# =========================
# configuracion de rutas
# =========================
# ruta absoluta de la carpeta donde se encuentra este script (.../scripts/)
directorio_script = os.path.dirname(os.path.abspath(__file__))

# construir la ruta del archivo xlsx en la carpeta data
ruta_dataset = os.path.join(directorio_script, "..", "data", "dataset.xlsx")


# =========================
# funciones de carga
# =========================
def cargar_excel_completo(ruta: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """
    carga todas las hojas del archivo excel y las retorna como diccionario.
    
    args:
        ruta: ruta al archivo excel. si es none, usa la ruta por defecto.
        
    returns:
        diccionario donde las claves son nombres de hojas y valores son dataframes.
        retorna none si hay error.
    """
    ruta_archivo = ruta if ruta else ruta_dataset
    print(f"cargando todas las hojas desde: {ruta_archivo}")
    
    try:
        # lee todas las hojas del excel como diccionario
        hojas = pd.read_excel(ruta_archivo, sheet_name=None)
        print(f"datos cargados exitosamente: {len(hojas)} hojas encontradas")
        
        # mostrar resumen de cada hoja
        for nombre_hoja, df in hojas.items():
            print(f"  - hoja '{nombre_hoja}': {df.shape[0]} filas, {df.shape[1]} columnas")
        
        return hojas
        
    except FileNotFoundError:
        print(f"error: el archivo no se encontro en: {ruta_archivo}")
        print("verifique que la ruta sea correcta y que el archivo exista en 'data/'.")
        return None
        
    except Exception as e:
        print(f"error al cargar los datos: {e}")
        return None


def cargar_hoja_individual(nombre_hoja: str, ruta: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    carga una hoja especifica del archivo excel.
    
    args:
        nombre_hoja: nombre de la hoja a cargar (ej: 'fifa 15', 'fifa 21')
        ruta: ruta al archivo excel. si es none, usa la ruta por defecto.
        
    returns:
        dataframe con los datos de la hoja.
        retorna none si hay error.
    """
    ruta_archivo = ruta if ruta else ruta_dataset
    print(f"cargando hoja '{nombre_hoja}' desde: {ruta_archivo}")
    
    try:
        df = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja)
        print(f"hoja cargada exitosamente: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
        
    except ValueError:
        print(f"error: la hoja '{nombre_hoja}' no existe en el archivo.")
        return None
        
    except FileNotFoundError:
        print(f"error: el archivo no se encontro en: {ruta_archivo}")
        return None
        
    except Exception as e:
        print(f"error al cargar la hoja: {e}")
        return None


def obtener_ruta_dataset() -> str:
    """
    retorna la ruta absoluta del archivo dataset.xlsx.
    
    returns:
        string con la ruta completa al archivo excel.
    """
    return os.path.abspath(ruta_dataset)


# =========================
# ejecucion directa
# =========================
if __name__ == "__main__":
    # prueba de carga cuando se ejecuta directamente
    print("=== prueba de cargador de datos fifa ===\n")
    print(f"directorio del script: {os.path.abspath(__file__)}")
    print(f"ruta del dataset: {obtener_ruta_dataset()}\n")
    
    # cargar todas las hojas
    diccionario_hojas = cargar_excel_completo()
    
    if diccionario_hojas is not None:
        # mostrar muestra de la primera hoja
        primer_hoja_nombre = list(diccionario_hojas.keys())[0]
        primer_hoja_df = diccionario_hojas[primer_hoja_nombre]
        
        print(f"\n=== muestra de la hoja '{primer_hoja_nombre}' ===")
        print(primer_hoja_df.head())
        
        print(f"\n=== informacion de la hoja '{primer_hoja_nombre}' ===")
        print(primer_hoja_df.info())
        
