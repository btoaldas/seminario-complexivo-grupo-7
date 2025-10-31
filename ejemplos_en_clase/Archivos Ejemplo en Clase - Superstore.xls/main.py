# %%
import os
from script.data_loader import cargar_datos_excel
from script.data_processing import union_dataframes, guardar_datos_procesados

# ruta absoluta de la carpeta donde está el script (.../scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# construir la ruta del archivo csv de data
EXCEL_PATH = os.path.join(SCRIPT_DIR, ".", "data", "Sample - Superstore.xls")

# ruta de salida (el csv consolidado)
PROCESSED_DATA_PATH = os.path.join(SCRIPT_DIR, "data", "processed", "superstore_consolidado.csv")
    
# ¿este archivo se está ejecutando directamente por el usuario o está siendo importado por otro script?
if __name__ == "__main__":
    # indica dónde está el script actual
    print(f"Ejecutando script desde: {os.path.abspath(__file__)}")
    
    hojas = ["Orders", "Returns", "People"]
    
    # llama a la función de arriba para cargar el csv
    diccionario_dataframes = cargar_datos_excel(EXCEL_PATH, hojas)
    
    if diccionario_dataframes is not None:
        
        # llama a la función de data_processing
        df_maestro_final = union_dataframes(diccionario_dataframes)     
        
        if df_maestro_final is not None:
            
            guardar_datos_procesados(df_maestro_final, PROCESSED_DATA_PATH)
            
            print("PROCESO DE UNIÓN Y GUARDADO FINALIZADO!!")
        
            print("\n---Primeras 5 filas de {nombre_hoja} ---")
            print(df_maestro_final.head())
            
            print("\n---Información del DataFrame de {nombre_hoja}---")
            df_maestro_final.info(show_counts=True)
            
        else: 
            print("ERROR en la unión de los datos")
            
    else: 
        print("Error en la carga de los datos")
            