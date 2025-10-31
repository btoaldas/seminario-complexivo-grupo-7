import pandas as pd

def cargar_datos(path):
    """
    carga el archivo Excel de FIFA (fifa.xlsx) con todas sus hojas
    correspondientes a las versiones FIFA 15, 16, 17, 18, 19, 20 y 21.
    une todas las hojas en un solo DataFrame y agrega una columna 'anio'
    para identificar de qué versión de FIFA proviene cada registro.
    
    parámetros:
        path: ruta al archivo fifa.xlsx
        
    retorna:
        DataFrame con todos los jugadores de FIFA 15-21 unidos
    """
    print(f"Cargando datos desde {path}...")
    
    try:
        # leer el archivo excel completo
        archivo_excel = pd.ExcelFile(path)
        
        # lista para almacenar cada hoja procesada
        lista_dataframes = []
        
        # procesar cada hoja del excel
        for nombre_hoja in archivo_excel.sheet_names:
            # leer la hoja actual
            df_hoja = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)
            
            # extraer el año del nombre de la hoja (ej: "FIFA 15" -> 2015)
            anio = int(nombre_hoja.split()[-1]) + 2000
            
            # agregar columna con el año para identificar la version
            df_hoja['anio'] = anio
            
            # agregar a la lista
            lista_dataframes.append(df_hoja)
        
        # unir todos los dataframes en uno solo
        df_completo = pd.concat(lista_dataframes, ignore_index=True)
        
        print(f"Datos cargados exitosamente. Total de registros: {len(df_completo)}")
        
        return df_completo
        
    except FileNotFoundError:
        print(f"Error: no se encontro el archivo en {path}")
        return None
    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}")
        return None
