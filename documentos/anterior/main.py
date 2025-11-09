# libreria general
import os
# funciones de los scripts
from scripts.data_loader import cargar_datos
from scripts.data_cleaning import (
    seleccionar_columnas_relevantes,
    renombrar_columnas_espaniol,
    eliminar_duplicados,
    eliminar_filas_valor_cero,
    convertir_fechas,
    limpiar_pie_preferido
)
from scripts.data_imputation import (
    imputar_valores_numericos,
    imputar_porteros,
    imputar_categoricos,
    imputar_valores_economicos
)
from scripts.data_new_features import (
    crear_categoria_edad,
    crear_categoria_valor,
    crear_diferencia_potencial,
    crear_posicion_principal,
    crear_imc,
    crear_promedio_atributos
)
from scripts.data_saving import guardar_datos_limpios

# ruta absoluta de la carpeta donde esta el script (raiz del proyecto)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# construir la ruta del archivo excel de data
DATA_PATH = os.path.join(SCRIPT_DIR, "data", "fifa.xlsx")

# nueva ruta de salida
PROCESSED_DATA_PATH = os.path.join(SCRIPT_DIR, "data", "processed", "fifa_limpio.csv")

# ¿este archivo se esta ejecutando directamente por el usuario o esta siendo importado por otro script?
if __name__ == "__main__":
    # indica donde esta el script actual
    print(f"Ejecutando script desde: {os.path.abspath(__file__)}")
    
    # llama a la funcion de arriba para cargar el excel
    dataframe_fifa = cargar_datos(DATA_PATH)
    
    if dataframe_fifa is not None:
        # MODULO LIMPIEZA DE DATOS
        print("\n---INICIANDO LIMPIEZA DE DATOS---")
        
        df_limpio = seleccionar_columnas_relevantes(dataframe_fifa)
        df_limpio = renombrar_columnas_espaniol(df_limpio)
        df_limpio = eliminar_duplicados(df_limpio)
        df_limpio = eliminar_filas_valor_cero(df_limpio)
        df_limpio = convertir_fechas(df_limpio)
        df_limpio = limpiar_pie_preferido(df_limpio)
        
        print("\n---LIMPIEZA DE DATOS TERMINADO---")
        
        # MODULO IMPUTACION DE DATOS
        print("\n---INICIANDO IMPUTACION DE DATOS---")
        
        df_procesado = imputar_valores_numericos(df_limpio)
        df_procesado = imputar_porteros(df_procesado)
        df_procesado = imputar_categoricos(df_procesado)
        df_procesado = imputar_valores_economicos(df_procesado)
        
        print("\n---IMPUTACION DE DATOS TERMINADO---")
        
        # MODULO NUEVAS COLUMNAS 
        print("\n---INICIANDO CREACION DE NUEVAS CARACTERISTICAS---")
        
        df_final = crear_categoria_edad(df_procesado)
        df_final = crear_categoria_valor(df_final)
        df_final = crear_diferencia_potencial(df_final)
        df_final = crear_posicion_principal(df_final)
        df_final = crear_imc(df_final)
        df_final = crear_promedio_atributos(df_final)
        
        print("\n---CREACION DE NUEVAS CARACTERISTICAS TERMINADO---")
        
        # GUARDAR DATOS
        guardar_datos_limpios(df_final, PROCESSED_DATA_PATH)
        
        # AQUI TERMINO EL PIPELINE DE LIMPIEZA
        print("\n---PIPELINE TERMINADO---")
        
        print("\n---Informacion del DataFrame---")
        df_final.info(show_counts=True)
        
    else: 
        print("Ha ocurrido un error en la carga de datos")
