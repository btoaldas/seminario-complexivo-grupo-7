"""
Módulo de Limpieza de Datos
Sistema de Scouting FIFA
"""

import pandas as pd


def seleccionar_columnas_relevantes(df):
    """
    Selecciona solo las columnas relevantes para el análisis.
    """
    print("\n" + "-"*60)
    print("SELECCIONANDO COLUMNAS RELEVANTES")
    print("-"*60)
    
    columnas_importantes = [
        'sofifa_id', 'player_url', 'short_name', 'long_name', 'age', 'dob',
        'height_cm', 'weight_kg', 'nationality', 'club_name', 'league_name',
        'player_positions', 'preferred_foot', 'weak_foot', 'skill_moves',
        'work_rate', 'body_type', 'real_face', 'overall', 'potential',
        'value_eur', 'wage_eur', 'release_clause_eur', 'international_reputation',
        'contract_valid_until', 'pace', 'shooting',
        'passing', 'dribbling', 'defending', 'physic', 'attacking_crossing',
        'attacking_finishing', 'attacking_heading_accuracy', 'attacking_short_passing',
        'attacking_volleys', 'skill_dribbling', 'skill_curve', 'skill_fk_accuracy',
        'skill_long_passing', 'skill_ball_control', 'movement_acceleration',
        'movement_sprint_speed', 'movement_agility', 'movement_reactions',
        'movement_balance', 'power_shot_power', 'power_jumping', 'power_stamina',
        'power_strength', 'power_long_shots', 'mentality_aggression',
        'mentality_interceptions', 'mentality_positioning', 'mentality_vision',
        'mentality_penalties', 'mentality_composure', 'defending_marking',
        'defending_standing_tackle', 'defending_sliding_tackle', 'goalkeeping_diving',
        'goalkeeping_handling', 'goalkeeping_kicking', 'goalkeeping_positioning',
        'goalkeeping_reflexes'
    ]
    
    if 'año_datos' in df.columns:
        columnas_importantes.append('año_datos')
    
    columnas_existentes = [col for col in columnas_importantes if col in df.columns]
    df_limpio = df[columnas_existentes].copy()
    
    print(f"   Columnas seleccionadas: {len(columnas_existentes)}")
    print("-"*60)
    
    return df_limpio


def eliminar_duplicados(df):
    """
    Elimina jugadores duplicados DENTRO DEL MISMO AÑO.
    """
    print("\n" + "-"*60)
    print("ELIMINANDO DUPLICADOS")
    print("-"*60)
    
    filas_antes = len(df)
    df_limpio = df.drop_duplicates(subset=['nombre_completo', 'año_datos'], keep='first')
    filas_despues = len(df_limpio)
    
    print(f"   Duplicados eliminados: {filas_antes - filas_despues:,}")
    print("-"*60)
    
    return df_limpio


def eliminar_columnas_muchos_nulos(df, umbral=0.5):
    """
    Elimina columnas con más de X% de valores nulos.
    """
    print("\n" + "-"*60)
    print("ELIMINANDO COLUMNAS CON EXCESO DE NULOS")
    print("-"*60)
    
    porcentaje_nulos = df.isnull().sum() / len(df)
    columnas_eliminar = porcentaje_nulos[porcentaje_nulos > umbral].index.tolist()
    df_limpio = df.drop(columns=columnas_eliminar)
    
    print(f"   Columnas eliminadas: {len(columnas_eliminar)}")
    print("-"*60)
    
    return df_limpio


def normalizar_valores_monetarios(df):
    """
    Normaliza columnas monetarias de formato string a numérico.
    """
    print("\n" + "-"*60)
    print("NORMALIZANDO VALORES MONETARIOS")
    print("-"*60)
    
    df_limpio = df.copy()
    columnas_monetarias = ['valor_mercado_eur', 'salario_eur', 'clausula_rescision_eur']
    
    for col in columnas_monetarias:
        if col in df_limpio.columns and df_limpio[col].dtype not in ['int64', 'float64']:
            def convertir_monetario(valor):
                if pd.isna(valor):
                    return valor
                valor_str = str(valor).replace('€', '').replace('$', '').strip()
                if 'M' in valor_str:
                    return float(valor_str.replace('M', '')) * 1_000_000
                elif 'K' in valor_str:
                    return float(valor_str.replace('K', '')) * 1_000
                else:
                    try:
                        return float(valor_str)
                    except:
                        return None
            
            df_limpio[col] = df_limpio[col].apply(convertir_monetario)
    
    print("   Columnas procesadas")
    print("-"*60)
    
    return df_limpio


def normalizar_fechas(df):
    """
    Normaliza columnas de fechas al formato datetime.
    """
    print("\n" + "-"*60)
    print("NORMALIZANDO FECHAS")
    print("-"*60)
    
    df_limpio = df.copy()
    if 'fecha_nacimiento' in df_limpio.columns:
        df_limpio['fecha_nacimiento'] = pd.to_datetime(df_limpio['fecha_nacimiento'], errors='coerce')
    
    print("   Fechas procesadas")
    print("-"*60)
    
    return df_limpio
