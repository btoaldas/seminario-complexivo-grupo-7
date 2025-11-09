import pandas as pd
import numpy as np

def imputar_valores_numericos(df):
    """
    imputa (rellena) valores faltantes en atributos numericos de jugadores
    como velocidad, tiro, pase, regate, defensa y fisico.
    usa la mediana agrupando por posicion principal para mayor precision.
    si quedan valores nulos, usa la mediana global de ese atributo.
    
    parámetros:
        df: DataFrame con valores faltantes en atributos
        
    retorna:
        DataFrame con valores numericos imputados
    """
    print("Iniciando imputacion de valores numericos...")
    
    # columnas de atributos numericos
    columnas_atributos = [
        'velocidad', 'tiro', 'pase', 'regate', 'defensa', 'fisico',
        'ataque_centros', 'ataque_definicion', 'ataque_precision_cabeza',
        'ataque_pase_corto', 'ataque_voleas',
        'habilidad_regate', 'habilidad_efecto', 'habilidad_tiros_libres',
        'habilidad_pase_largo', 'habilidad_control_balon',
        'movimiento_aceleracion', 'movimiento_velocidad_sprint', 'movimiento_agilidad',
        'movimiento_reacciones', 'movimiento_equilibrio',
        'potencia_tiro', 'potencia_salto', 'potencia_resistencia',
        'potencia_fuerza', 'potencia_tiros_lejanos',
        'mentalidad_agresividad', 'mentalidad_interceptaciones', 'mentalidad_posicionamiento',
        'mentalidad_vision', 'mentalidad_penales', 'mentalidad_compostura',
        'defensa_marcaje', 'defensa_entrada_parado', 'defensa_entrada_deslizante'
    ]
    
    # filtrar solo las que existen
    columnas_existentes = [col for col in columnas_atributos if col in df.columns]
    
    for columna in columnas_existentes:
        if df[columna].isna().sum() > 0:
            # imputar con la mediana de la posicion si existe
            if 'posiciones' in df.columns:
                # extraer primera posicion para agrupar
                df['posicion_principal'] = df['posiciones'].str.split(',').str[0].str.strip()
                
                # imputar por posicion
                df[columna] = df.groupby('posicion_principal')[columna].transform(
                    lambda x: x.fillna(x.median())
                )
            
            # si aun quedan nulos, usar mediana global
            df[columna] = df[columna].fillna(df[columna].median())
    
    # eliminar columna temporal si fue creada
    if 'posicion_principal' in df.columns:
        df = df.drop(columns=['posicion_principal'])
    
    print("Imputacion de valores numericos completada.")
    
    return df


def imputar_porteros(df):
    """
    imputa valores de atributos especificos de porteria (estiradas, manejo,
    saque, posicionamiento, reflejos). para jugadores que NO son porteros,
    asigna 0. para porteros sin datos, usa la mediana de todos los porteros.
    
    parámetros:
        df: DataFrame con valores faltantes en atributos de porteria
        
    retorna:
        DataFrame con valores de porteria imputados
    """
    print("Iniciando imputacion de atributos de porteria...")
    
    columnas_porteria = [
        'porteria_estiradas', 'porteria_manejo', 'porteria_saque',
        'porteria_posicionamiento', 'porteria_reflejos'
    ]
    
    # filtrar solo las columnas que existen en el dataframe
    columnas_existentes = [col for col in columnas_porteria if col in df.columns]
    
    for columna in columnas_existentes:
        if df[columna].isna().sum() > 0:
            # identificar quien es portero (posicion contiene 'GK')
            es_portero = df['posiciones'].str.contains('GK', na=False)
            
            # para no porteros, asignar 0
            df.loc[~es_portero, columna] = df.loc[~es_portero, columna].fillna(0)
            
            # para porteros, imputar con mediana de porteros
            mediana_porteros = df.loc[es_portero, columna].median()
            df.loc[es_portero, columna] = df.loc[es_portero, columna].fillna(mediana_porteros)
    
    print("Imputacion de atributos de porteria completada.")
    
    return df


def imputar_categoricos(df):
    """
    imputa valores faltantes en columnas categoricas como pie preferido,
    ritmo de trabajo, tipo de cuerpo, club y liga. usa la moda para
    pie preferido y valores por defecto razonables para el resto.
    
    parámetros:
        df: DataFrame con valores categoricos faltantes
        
    retorna:
        DataFrame con categorias imputadas
    """
    print("Iniciando imputacion de valores categoricos...")
    
    # pie preferido: usar la moda (Right es mas comun)
    if 'pie_preferido' in df.columns and df['pie_preferido'].isna().sum() > 0:
        moda = df['pie_preferido'].mode()[0]
        df['pie_preferido'] = df['pie_preferido'].fillna(moda)
    
    # ritmo de trabajo: usar valor medio
    if 'ritmo_trabajo' in df.columns and df['ritmo_trabajo'].isna().sum() > 0:
        df['ritmo_trabajo'] = df['ritmo_trabajo'].fillna('Medium / Medium')
    
    # tipo de cuerpo: usar Normal
    if 'tipo_cuerpo' in df.columns and df['tipo_cuerpo'].isna().sum() > 0:
        df['tipo_cuerpo'] = df['tipo_cuerpo'].fillna('Normal')
    
    # club: asignar 'Sin Club' para jugadores libres
    if 'club' in df.columns and df['club'].isna().sum() > 0:
        df['club'] = df['club'].fillna('Sin Club')
    
    # liga: asignar 'Sin Liga' para jugadores sin liga
    if 'liga' in df.columns and df['liga'].isna().sum() > 0:
        df['liga'] = df['liga'].fillna('Sin Liga')
    
    print("Imputacion de valores categoricos completada.")
    
    return df


def imputar_valores_economicos(df):
    """
    imputa valores faltantes en salario_euros y clausula_rescision_euros.
    para salario, agrupa por rangos de calificacion general y usa la mediana.
    para clausula de rescision, usa mediana global si tiene menos del 50% nulos.
    NO imputa valor_euros porque es la variable objetivo del modelo.
    
    parámetros:
        df: DataFrame con valores economicos faltantes
        
    retorna:
        DataFrame con valores economicos imputados
    """
    print("Iniciando imputacion de valores economicos...")
    
    # salario: imputar con mediana agrupando por calificacion
    if 'salario_euros' in df.columns and df['salario_euros'].isna().sum() > 0:
        # crear rangos de calificacion para agrupar
        df['rango_calificacion'] = pd.cut(
            df['calificacion_general'],
            bins=[0, 60, 70, 80, 90, 100],
            labels=['Bajo', 'Medio', 'Bueno', 'Muy Bueno', 'Elite']
        )
        
        # imputar por rango de calificacion
        df['salario_euros'] = df.groupby('rango_calificacion')['salario_euros'].transform(
            lambda x: x.fillna(x.median())
        )
        
        # si quedan nulos, usar mediana global
        df['salario_euros'] = df['salario_euros'].fillna(df['salario_euros'].median())
        
        # eliminar columna temporal
        df = df.drop(columns=['rango_calificacion'])
    
    # clausula de rescision: imputar solo si hay suficientes datos
    if 'clausula_rescision_euros' in df.columns:
        nulos = df['clausula_rescision_euros'].isna().sum()
        porcentaje_nulos = (nulos / len(df)) * 100
        
        # imputar solo si tiene menos del 50% de nulos
        if porcentaje_nulos < 50:
            df['clausula_rescision_euros'] = df['clausula_rescision_euros'].fillna(
                df['clausula_rescision_euros'].median()
            )
    
    print("Imputacion de valores economicos completada.")
    
    return df
