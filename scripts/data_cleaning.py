import pandas as pd
import numpy as np

def seleccionar_columnas_relevantes(df):
    """
    selecciona solo las columnas mas relevantes para el analisis y prediccion
    de valor de mercado de jugadores. elimina columnas innecesarias como URLs,
    IDs de sofifa, y atributos de posiciones especificas (ls, st, rs, etc.)
    que no aportan al modelo de prediccion.
    
    parámetros:
        df: DataFrame con todas las columnas originales del dataset
        
    retorna:
        DataFrame filtrado solo con columnas relevantes
    """
    print("Seleccionando columnas relevantes...")
    
    # columnas a mantener para el analisis
    columnas_mantener = [
        # identificacion basica
        'short_name', 'long_name', 'age', 'dob',
        # fisico
        'height_cm', 'weight_kg',
        # ubicacion y club
        'nationality', 'club_name', 'league_name', 'league_rank',
        # habilidades principales
        'overall', 'potential',
        # economia (VARIABLE OBJETIVO)
        'value_eur', 'wage_eur', 'release_clause_eur',
        # posicion y caracteristicas
        'player_positions', 'preferred_foot', 'international_reputation',
        'weak_foot', 'skill_moves', 'work_rate', 'body_type',
        # contrato
        'joined', 'contract_valid_until',
        # atributos principales (6 categorias)
        'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic',
        # atributos detallados de ataque
        'attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy',
        'attacking_short_passing', 'attacking_volleys',
        # atributos de habilidad
        'skill_dribbling', 'skill_curve', 'skill_fk_accuracy',
        'skill_long_passing', 'skill_ball_control',
        # atributos de movimiento
        'movement_acceleration', 'movement_sprint_speed', 'movement_agility',
        'movement_reactions', 'movement_balance',
        # atributos de potencia
        'power_shot_power', 'power_jumping', 'power_stamina',
        'power_strength', 'power_long_shots',
        # mentalidad
        'mentality_aggression', 'mentality_interceptions', 'mentality_positioning',
        'mentality_vision', 'mentality_penalties', 'mentality_composure',
        # defensa
        'defending_marking', 'defending_standing_tackle', 'defending_sliding_tackle',
        # porteria (para porteros)
        'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking',
        'goalkeeping_positioning', 'goalkeeping_reflexes',
        # año (agregado por nosotros)
        'anio'
    ]
    
    # seleccionar solo las columnas que existen en el dataframe
    columnas_existentes = [col for col in columnas_mantener if col in df.columns]
    df_filtrado = df[columnas_existentes].copy()
    
    print(f"Columnas filtradas: {len(df_filtrado.columns)} de {len(df.columns)} originales.")
    
    return df_filtrado


def renombrar_columnas_espaniol(df):
    """
    renombra todas las columnas del ingles al espanol usando nombres
    descriptivos que faciliten la comprension del dataset.
    usa snake_case en minusculas sin tildes para mantener consistencia.
    
    parámetros:
        df: DataFrame con nombres de columnas en ingles
        
    retorna:
        DataFrame con nombres de columnas en espanol
    """
    print("Renombrando columnas a espanol...")
    
    # diccionario de traduccion
    traducciones = {
        # basico
        'short_name': 'nombre_corto',
        'long_name': 'nombre_completo',
        'age': 'edad',
        'dob': 'fecha_nacimiento',
        'height_cm': 'altura_cm',
        'weight_kg': 'peso_kg',
        'nationality': 'nacionalidad',
        'club_name': 'club',
        'league_name': 'liga',
        'league_rank': 'ranking_liga',
        'overall': 'calificacion_general',
        'potential': 'potencial',
        'value_eur': 'valor_euros',
        'wage_eur': 'salario_euros',
        'release_clause_eur': 'clausula_rescision_euros',
        'player_positions': 'posiciones',
        'preferred_foot': 'pie_preferido',
        'international_reputation': 'reputacion_internacional',
        'weak_foot': 'pie_debil',
        'skill_moves': 'habilidades_movimiento',
        'work_rate': 'ritmo_trabajo',
        'body_type': 'tipo_cuerpo',
        'joined': 'fecha_ingreso_club',
        'contract_valid_until': 'contrato_hasta',
        # atributos principales
        'pace': 'velocidad',
        'shooting': 'tiro',
        'passing': 'pase',
        'dribbling': 'regate',
        'defending': 'defensa',
        'physic': 'fisico',
        # ataque
        'attacking_crossing': 'ataque_centros',
        'attacking_finishing': 'ataque_definicion',
        'attacking_heading_accuracy': 'ataque_precision_cabeza',
        'attacking_short_passing': 'ataque_pase_corto',
        'attacking_volleys': 'ataque_voleas',
        # habilidad
        'skill_dribbling': 'habilidad_regate',
        'skill_curve': 'habilidad_efecto',
        'skill_fk_accuracy': 'habilidad_tiros_libres',
        'skill_long_passing': 'habilidad_pase_largo',
        'skill_ball_control': 'habilidad_control_balon',
        # movimiento
        'movement_acceleration': 'movimiento_aceleracion',
        'movement_sprint_speed': 'movimiento_velocidad_sprint',
        'movement_agility': 'movimiento_agilidad',
        'movement_reactions': 'movimiento_reacciones',
        'movement_balance': 'movimiento_equilibrio',
        # potencia
        'power_shot_power': 'potencia_tiro',
        'power_jumping': 'potencia_salto',
        'power_stamina': 'potencia_resistencia',
        'power_strength': 'potencia_fuerza',
        'power_long_shots': 'potencia_tiros_lejanos',
        # mentalidad
        'mentality_aggression': 'mentalidad_agresividad',
        'mentality_interceptions': 'mentalidad_interceptaciones',
        'mentality_positioning': 'mentalidad_posicionamiento',
        'mentality_vision': 'mentalidad_vision',
        'mentality_penalties': 'mentalidad_penales',
        'mentality_composure': 'mentalidad_compostura',
        # defensa detallada
        'defending_marking': 'defensa_marcaje',
        'defending_standing_tackle': 'defensa_entrada_parado',
        'defending_sliding_tackle': 'defensa_entrada_deslizante',
        # porteria
        'goalkeeping_diving': 'porteria_estiradas',
        'goalkeeping_handling': 'porteria_manejo',
        'goalkeeping_kicking': 'porteria_saque',
        'goalkeeping_positioning': 'porteria_posicionamiento',
        'goalkeeping_reflexes': 'porteria_reflejos',
        # año
        'anio': 'anio'
    }
    
    # renombrar solo las columnas que existen en el dataframe
    columnas_renombrar = {k: v for k, v in traducciones.items() if k in df.columns}
    df_renombrado = df.rename(columns=columnas_renombrar)
    
    print("Nombres de columnas actualizados.")
    
    return df_renombrado


def eliminar_duplicados(df):
    """
    elimina registros duplicados de jugadores basandose en nombre completo y año.
    cuando hay duplicados, conserva el registro con mayor calificacion general.
    esto asegura que mantenemos la mejor version de cada jugador por temporada.
    
    parámetros:
        df: DataFrame que puede contener jugadores duplicados
        
    retorna:
        DataFrame sin duplicados
    """
    print("Eliminando duplicados...")
    
    filas_antes = len(df)
    
    # ordenar por calificacion general descendente para mantener el mejor registro
    df_ordenado = df.sort_values('calificacion_general', ascending=False)
    
    # eliminar duplicados manteniendo el primero (mayor calificacion)
    df_sin_duplicados = df_ordenado.drop_duplicates(
        subset=['nombre_completo', 'anio'],
        keep='first'
    ).copy()
    
    filas_despues = len(df_sin_duplicados)
    
    print(f"Duplicados eliminados. Filas antes: {filas_antes} - despues: {filas_despues}")
    
    return df_sin_duplicados


def eliminar_filas_valor_cero(df):
    """
    elimina jugadores que tienen valor de mercado igual a 0 o nulo.
    estos registros no son utiles para entrenar un modelo de prediccion
    de valor, ya que no tienen la variable objetivo definida.
    
    parámetros:
        df: DataFrame original
        
    retorna:
        DataFrame sin registros con valor 0 o nulo
    """
    print("Eliminando jugadores sin valor de mercado...")
    
    filas_antes = len(df)
    
    # filtrar donde valor_euros es mayor a 0 y no es nulo
    df_filtrado = df[
        (df['valor_euros'].notna()) & 
        (df['valor_euros'] > 0)
    ].copy()
    
    filas_despues = len(df_filtrado)
    
    print(f"Filas eliminadas: {filas_antes - filas_despues}")
    
    return df_filtrado


def convertir_fechas(df):
    """
    convierte las columnas de fechas (fecha_nacimiento, fecha_ingreso_club)
    de formato string a tipo datetime para permitir operaciones temporales.
    
    parámetros:
        df: DataFrame con fechas como string
        
    retorna:
        DataFrame con fechas convertidas a datetime
    """
    print("Convirtiendo columnas de fechas a datetime...")
    
    columnas_fecha = ['fecha_nacimiento', 'fecha_ingreso_club']
    
    for columna in columnas_fecha:
        if columna in df.columns:
            df[columna] = pd.to_datetime(df[columna], errors='coerce')
    
    print("Fechas convertidas.")
    
    return df


def limpiar_pie_preferido(df):
    """
    normaliza los valores de la columna pie_preferido (Left/Right)
    eliminando espacios y estandarizando el formato con mayusculas iniciales.
    
    parámetros:
        df: DataFrame original
        
    retorna:
        DataFrame con pie_preferido normalizado
    """
    print("Normalizando pie preferido...")
    
    if 'pie_preferido' in df.columns:
        # normalizar formato: eliminar espacios y capitalizar
        df['pie_preferido'] = df['pie_preferido'].str.strip().str.title()
    
    return df
