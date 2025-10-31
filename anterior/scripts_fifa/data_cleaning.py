import pandas as pd
import numpy as np

def limpieza_nombres_columnas(df):
    """
    toma un df, renombra las columnas específicas del dataset FIFA y luego
    convierte todos los nombres de la columna en minúsculas
    """
    print("Iniciando limpieza de nombres de columnas...")
    
    df_renombrado = df.rename(
        columns={
            "short_name": "nombre", 
            "player_positions": "posicion",
            "club_name": "club",
            "league_name": "liga",
            "value_eur": "valor_mercado",
            "wage_eur": "salario"
        }
    )
    
    df_renombrado.columns = df_renombrado.columns.str.lower()
    
    print("Nombres de columnas limpias.")
    
    return df_renombrado



def convertir_edad_int(df):
    """
    convierte 'age' (edad) de int64 a Int64 asegurando manejo de nulos
    """
    print("Convirtiendo 'age' a Int64...")
    
    df["age"] = df["age"].astype("Int64")
    
    return df


def limpieza_valores_monetarios(df):
    """
    asegura que las columnas de valor de mercado y salario (value_eur, wage_eur)
    estén en formato numérico correcto y maneja valores faltantes
    """
    print("Limpiando valores monetarios (valor_mercado y salario)...")
    
    # asegurar que sean float64 y manejar posibles nulos
    df["valor_mercado"] = pd.to_numeric(df["valor_mercado"], errors='coerce')
    df["salario"] = pd.to_numeric(df["salario"], errors='coerce')
    
    return df


def eliminar_filas_info_faltantes(df):
    """
    elimina filas que no contienen información 
    en la mayoría de columnas críticas del dataset FIFA
    primero: 'nombre' y 'posicion' (datos fundamentales del jugador)
    luego: 'overall', 'potential', 'valor_mercado', 'club'
    """
    print("Iniciando eliminación de filas con información faltante...")
    
    df_limpio = df.dropna(
        subset=["nombre", "posicion"], 
        how="all"
    )
    
    df_limpio = df_limpio.dropna(
        subset=["overall", "potential", "valor_mercado", "club"], 
        how="all"
    )
    
    df_limpio = df_limpio.reset_index(drop=True)
    
    print(f"Las filas han sido eliminadas. Tamaño del DataFrame antes: {len(df)} - después {len(df_limpio)}.")
    
    return df_limpio


def rellenar_valores_club(df):
    """
    en la columna 'club' rellena los NaNs
    con 'Sin Club' (Free Agent), asumiendo que si no hay valor
    el jugador está sin club o es agente libre
    """
    print("Iniciando limpieza de 'NaN' en 'club' con valor 'Sin Club'...")
    
    df["club"] = df["club"].fillna("Sin Club")
    
    return df


def agregar_columna_anio(df, anio):
    """
    agrega una columna 'anio' al dataframe con el año de la versión de FIFA
    útil cuando se concatenan múltiples hojas del dataset
    """
    print(f"Agregando columna 'anio' con valor {anio}...")
    
    df["anio"] = anio
    
    return df


def eliminar_duplicados(df):
    """
    elimina jugadores duplicados basándose en 'sofifa_id'
    mantiene la primera ocurrencia
    """
    print("Eliminando jugadores duplicados...")
    
    filas_antes = len(df)
    df_sin_duplicados = df.drop_duplicates(subset=['sofifa_id'], keep='first')
    df_sin_duplicados = df_sin_duplicados.reset_index(drop=True)
    
    filas_eliminadas = filas_antes - len(df_sin_duplicados)
    print(f"Duplicados eliminados: {filas_eliminadas}. Tamaño del DataFrame: {len(df_sin_duplicados)}.")
    
    return df_sin_duplicados


def validar_rangos_numericos(df):
    """
    valida que los valores numéricos clave estén en rangos lógicos
    - edad: entre 15 y 45 años
    - overall y potential: entre 0 y 100
    - valor_mercado y salario: no negativos
    """
    print("Validando rangos numéricos...")
    
    # filtrar edades válidas
    df = df[(df['age'] >= 15) & (df['age'] <= 45)]
    
    # filtrar overall y potential válidos
    df = df[(df['overall'] >= 0) & (df['overall'] <= 100)]
    df = df[(df['potential'] >= 0) & (df['potential'] <= 100)]
    
    # filtrar valores monetarios no negativos
    df = df[(df['valor_mercado'] >= 0) & (df['salario'] >= 0)]
    
    df = df.reset_index(drop=True)
    
    print(f"Validación completada. Filas válidas: {len(df)}.")
    
    return df