import pandas as pd
import numpy as np

def crear_categoria_edad(df):
    """
    crea una nueva columna 'categoria_edad' que clasifica a los jugadores
    en rangos de edad: Promesa (<=21), Joven (22-25), Consolidado (26-30),
    Veterano (31-35) y Leyenda (>35). util para analisis y visualizacion.
    
    parámetros:
        df: DataFrame con columna edad
        
    retorna:
        DataFrame con nueva columna categoria_edad
    """
    print("Creando categoria de edad...")
    
    if 'edad' in df.columns:
        df['categoria_edad'] = pd.cut(
            df['edad'],
            bins=[0, 21, 25, 30, 35, 100],
            labels=['Promesa', 'Joven', 'Consolidado', 'Veterano', 'Leyenda']
        )
    
    return df


def crear_categoria_valor(df):
    """
    crea una nueva columna 'categoria_valor' que clasifica el valor de mercado
    en rangos: Bajo (<1M), Medio (1-5M), Alto (5-20M), Muy Alto (20-50M)
    y Elite (>50M euros). facilita el analisis por segmentos de valor.
    
    parámetros:
        df: DataFrame con columna valor_euros
        
    retorna:
        DataFrame con nueva columna categoria_valor
    """
    print("Creando categoria de valor...")
    
    if 'valor_euros' in df.columns:
        df['categoria_valor'] = pd.cut(
            df['valor_euros'],
            bins=[0, 1_000_000, 5_000_000, 20_000_000, 50_000_000, np.inf],
            labels=['Bajo', 'Medio', 'Alto', 'Muy Alto', 'Elite']
        )
    
    return df


def crear_diferencia_potencial(df):
    """
    crea la columna 'margen_crecimiento' que calcula la diferencia entre
    el potencial y la calificacion actual del jugador. indica cuanto puede
    mejorar aun. valores altos = jugadores jovenes con mucho potencial.
    
    parámetros:
        df: DataFrame con columnas potencial y calificacion_general
        
    retorna:
        DataFrame con nueva columna margen_crecimiento
    """
    print("Creando margen de crecimiento...")
    
    if 'potencial' in df.columns and 'calificacion_general' in df.columns:
        df['margen_crecimiento'] = df['potencial'] - df['calificacion_general']
    
    return df


def crear_posicion_principal(df):
    """
    extrae la posicion principal del jugador tomando la primera posicion
    de la lista de posiciones. ejemplo: "ST, CF" -> "ST"
    
    parámetros:
        df: DataFrame con columna posiciones
        
    retorna:
        DataFrame con nueva columna posicion_principal
    """
    print("Extrayendo posicion principal...")
    
    if 'posiciones' in df.columns:
        df['posicion_principal'] = df['posiciones'].str.split(',').str[0].str.strip()
    
    return df


def crear_imc(df):
    """
    calcula el Indice de Masa Corporal (IMC) de cada jugador usando la
    formula: IMC = peso_kg / (altura_m)^2
    util para analisis fisico de jugadores.
    
    parámetros:
        df: DataFrame con columnas altura_cm y peso_kg
        
    retorna:
        DataFrame con nueva columna imc
    """
    print("Calculando IMC...")
    
    if 'altura_cm' in df.columns and 'peso_kg' in df.columns:
        # convertir altura de cm a metros
        altura_m = df['altura_cm'] / 100
        
        # calcular imc
        df['imc'] = df['peso_kg'] / (altura_m ** 2)
    
    return df


def crear_promedio_atributos(df):
    """
    calcula el promedio de los 6 atributos principales del jugador:
    velocidad, tiro, pase, regate, defensa y fisico.
    sirve como un resumen general de las habilidades del jugador.
    
    parámetros:
        df: DataFrame con atributos principales
        
    retorna:
        DataFrame con nueva columna promedio_atributos
    """
    print("Calculando promedio de atributos principales...")
    
    atributos = ['velocidad', 'tiro', 'pase', 'regate', 'defensa', 'fisico']
    atributos_existentes = [col for col in atributos if col in df.columns]
    
    if len(atributos_existentes) >= 4:
        df['promedio_atributos'] = df[atributos_existentes].mean(axis=1)
    
    return df
