# scripts_fifa/data_merge.py 
import pandas as pd
from scripts_fifa.data_loader import cargar_datos_excel

# consolidar datos de varias hojas en un solo DataFrame
def union_dataframes(dataframes):
    try:
        df_fifa15 = dataframes["FIFA 15"]
        df_fifa16 = dataframes["FIFA 16"]
        df_fifa17 = dataframes["FIFA 17"]
        df_fifa18 = dataframes["FIFA 18"]
        df_fifa19 = dataframes["FIFA 19"]
        df_fifa20 = dataframes["FIFA 20"]
        df_fifa21 = dataframes["FIFA 21"]
        
        df_maestro = pd.merge(
            df_fifa15,
            df_fifa16,
            df_fifa17,
            df_fifa18,
            df_fifa19,
            df_fifa20,
            df_fifa21,
            on="ID",
            suffixes=("_15", "_16", "_17", "_18", "_19", "_20", "_21"),
            how="outer"
        )
        
        df_maestro["Returned"] = df_maestro["Returned"].fillna("No")
        
        print("Listo. Ahora se esta uniendo los datos en un solo DataFrame maestro.")
        
        df_maestro = pd.merge(
            left =df_fifa15,
            right=df_maestro,
            on="ID",
            how="left"
        )
        
        print("Unión completada exitosamente.")
        return df_maestro
    except Exception as e:
        print(f"Error al unir los DataFrames: {e}")
        return None
        
        