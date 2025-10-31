# la impiutacion de datos en el dataset de FIFA
import pandas as pd

def imputar_datos(df):
    """
    Imputa datos faltantes en el DataFrame de FIFA.
    
    args:
        df: DataFrame a imputar
        
    returns:
        DataFrame con datos imputados
    """
    df = df.copy()
    df = df.fillna({
        "user_score": df["user_score"].median(),
        "esrb_rating": "Not Rated"
    })
    return df
def imputar_valores_numericos(df, columnas):
    """
    Imputa valores faltantes en columnas numéricas con la mediana de cada columna.
    
    args:
        df: DataFrame a imputar
        columnas: lista de nombres de columnas a imputar
        
    returns:
        DataFrame con valores imputados
    """
    df = df.copy()
    for col in columnas:
        df[col] = df[col].fillna(df[col].median())
    return df