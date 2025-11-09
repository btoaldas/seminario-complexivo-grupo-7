import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


def preparar_datos_modelo(df):
    """
    toma el df_limpio, aplica el OneHotEncoding y devuelve X, y, el encoder
    """
    print("Iniciando preparación de X/y...")
    
    # CONFIGURACIÓN OPTIMIZADA BASADA EN EDA REAL (122,501 jugadores, 73 columnas)
    col_categoricas = [
        "categoria_posicion",     # 4 categorías
        "categoria_edad",         # 3 categorías
        "pie_preferido",          # 2 categorías
        "categoria_reputacion",   # 5 categorías - NUEVA
        "liga"                    # 56 categorías - NUEVA (confirmado por EDA)
    ]
    
    col_numericas = [
        # TOP FEATURES - CORRELACIÓN FUERTE (> 0.50) - Confirmado por EDA
        "reputacion_internacional",  # 0.6423 - NUEVA (Diferencia 52x entre nivel 1 y 5)
        "valoracion_global",          # 0.6067
        "potencial",                  # 0.5631
        "movimiento_reacciones",      # 0.5178
        
        # FEATURES MODERADAS (0.30 - 0.50)
        "calidad_promedio",           # 0.4560 - Feature ingenierada
        "pase",                       # 0.3983
        "mentalidad_compostura",      # 0.3856
        "regate_gambeta",             # 0.3849
        "mentalidad_vision",          # 0.3341
        "tiro_disparo",               # 0.3129
        "ataque_pase_corto",          # 0.3086
        
        # FEATURES ADICIONALES RELEVANTES
        "ataque_definicion",
        "ataque_cabezazo",
        "ataque_centros",
        "ataque_voleas",
        
        # Atributos físicos
        "movimiento_velocidad_sprint",
        "movimiento_aceleracion",
        "movimiento_agilidad",
        "movimiento_equilibrio",
        "fisico",
        
        # Atributos defensivos
        "defensa",
        "defensa_entrada_pie",
        "defensa_entrada_deslizante",
        "defensa_marcaje",
        
        # Atributos mentales
        "mentalidad_agresividad",
        "mentalidad_intercepciones",
        "mentalidad_posicionamiento",
        "mentalidad_penales",
        
        # Habilidades
        "pie_debil",
        "habilidades_regate",
        "habilidad_regate",
        "habilidad_control_balon",
        "habilidad_efecto",
        "habilidad_pase_largo",
        "habilidad_tiros_libres",
        
        # FEATURES CALCULADAS - NUEVAS
        "diferencia_potencial",
        "ratio_valor_salario",        # 0.1199 - NUEVA (Previene data leakage de salario_eur)
        "anos_contrato_restantes",    # 0.1267 - NUEVA (Contexto contractual)
        
        # Demografía
        "edad"                        # 0.0866
    ]
    
    target = "valor_mercado_eur"

    X_categoricas = df[col_categoricas]
    X_numericas = df[col_numericas].copy()
    
    # aplicar transformación logarítmica al target
    print("Aplicando transformación log1p al target...")
    y = np.log1p(df[target])

    # TARGET ENCODING PARA CLUB (954 clubes - confirmado por EDA)
    # Club marca diferencia 15-20x: Bayern €24.23M vs promedio €2M
    print("Aplicando Target Encoding para club (954 categorías)...")
    club_encoding = df.groupby('club')[target].mean()
    X_numericas['club_valor_promedio'] = df['club'].map(club_encoding)
    # Rellenar clubes desconocidos con la mediana global
    X_numericas['club_valor_promedio'].fillna(df[target].median(), inplace=True)
    print(f"  - Top 3 clubes: Bayern €{club_encoding.nlargest(1).values[0]/1e6:.2f}M, "
          f"Barça €{club_encoding.nlargest(2).values[1]/1e6:.2f}M, "
          f"Madrid €{club_encoding.nlargest(3).values[2]/1e6:.2f}M")

    # aplicar el OneHotEncoding para el resto de categóricas
    print("Aplicando OneHotEncoder para categóricas...")
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X_categoricas_encoded = encoder.fit_transform(X_categoricas)

    nuevas_columnas = encoder.get_feature_names_out(col_categoricas)

    df_encoded = pd.DataFrame(
        X_categoricas_encoded, 
        columns = nuevas_columnas
    )

    X = pd.concat([X_numericas.reset_index(drop=True), df_encoded], axis=1)
    
    print("\n" + "=" * 70)
    print("RESUMEN DE FEATURES PREPARADAS:")
    print("=" * 70)
    print(f"Features numéricas base:                  {len(col_numericas)}")
    print(f"Features numéricas + club_valor_promedio: {len(col_numericas) + 1}")
    print(f"Features categóricas (5 variables):       {len(col_categoricas)}")
    print(f"Features categóricas después OneHot:      {X.shape[1] - (len(col_numericas) + 1)}")
    print(f"TOTAL FEATURES FINALES:                   {X.shape[1]}")
    print(f"Jugadores (registros):                    {X.shape[0]:,}")
    print(f"Target transformado: log1p(valor_mercado_eur)")
    print("=" * 70)
    print(f"\nPreparación completa. X: {X.shape}, y: {y.shape}")
    
    return X, y, encoder, club_encoding


def dividir_datos(X, y): 
    """
    aplica train_test_split con los parámetros definidos
    """
    
    RANDOM_STATE = 42
    TEST_SIZE = 0.25
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    print(f"Tamaño X_train: {X_train.shape}, tamaño X_test: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test


def codificar_variables_categoricas(X_train, X_test):
    """
    Aplica OneHotEncoding a variables categóricas.
    
    Args:
        X_train: Features de entrenamiento
        X_test: Features de prueba
        
    Returns:
        X_train_encoded, X_test_encoded, encoder
    """
    # Identificar columnas categóricas
    columnas_categoricas = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    columnas_numericas = X_train.select_dtypes(include=[np.number]).columns.tolist()
    
    if not columnas_categoricas:
        print("OK: No hay variables categóricas para codificar")
        return X_train, X_test, None
    
    # Limitar categorías para evitar explosión dimensional
    columnas_usar = []
    for col in columnas_categoricas:
        n_categorias = X_train[col].nunique()
        if n_categorias <= 50:  # Máximo 50 categorías únicas
            columnas_usar.append(col)
    
    if not columnas_usar:
        X_train_final = X_train[columnas_numericas]
        X_test_final = X_test[columnas_numericas]
        print("OK: Todas las variables categóricas tienen demasiadas categorías, se omiten")
        return X_train_final, X_test_final, None
    
    # Crear encoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    
    # Ajustar y transformar train
    encoded_train = encoder.fit_transform(X_train[columnas_usar])
    encoded_test = encoder.transform(X_test[columnas_usar])
    
    # Crear DataFrames con nombres de columnas
    feature_names = encoder.get_feature_names_out(columnas_usar)
    df_encoded_train = pd.DataFrame(encoded_train, columns=feature_names, index=X_train.index)
    df_encoded_test = pd.DataFrame(encoded_test, columns=feature_names, index=X_test.index)
    
    # Combinar con columnas numéricas
    X_train_final = pd.concat([X_train[columnas_numericas], df_encoded_train], axis=1)
    X_test_final = pd.concat([X_test[columnas_numericas], df_encoded_test], axis=1)
    
    print(f"OK: Encoding completado")
    print(f"  Columnas originales: {len(columnas_numericas) + len(columnas_usar)}")
    print(f"  Columnas finales: {X_train_final.shape[1]}")
    
    return X_train_final, X_test_final, encoder
