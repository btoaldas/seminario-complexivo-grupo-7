"""
Script para pre-calcular predicciones ML de todos los jugadores
Genera CSV con clasificaciones (Infravalorado/Sobrevalorado/Justo)
"""

import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from datetime import datetime
import sys

# Agregar path del backend al sys.path
sys.path.append(str(Path(__file__).parent.parent))

def generar_predicciones_ml(tolerancia_porcentaje=8.0):
    """
    Genera CSV con predicciones ML para todos los jugadores
    
    Args:
        tolerancia_porcentaje: Porcentaje de diferencia para clasificar (default 8%)
    
    Returns:
        DataFrame con predicciones
    """
    print("="*70)
    print(f"🤖 GENERADOR DE PREDICCIONES ML")
    print(f"📊 Tolerancia: {tolerancia_porcentaje}%")
    print("="*70)
    
    # Rutas
    base_path = Path(__file__).parent.parent.parent.parent
    data_path = base_path / 'datos' / 'procesados'
    models_path = base_path / 'datos' / 'modelos'
    
    # 1. Cargar dataset limpio
    print("\n📂 Cargando dataset...")
    df_jugadores = pd.read_csv(data_path / 'fifa_limpio.csv')
    print(f"   ✅ Cargados {len(df_jugadores):,} registros")
    
    # 2. Cargar modelo, encoder y club_encoding
    print("\n🤖 Cargando modelo ML y transformadores...")
    try:
        modelo = joblib.load(models_path / 'modelo_fifa.joblib')
        encoder = joblib.load(models_path / 'encoder_fifa.joblib')
        club_encoding = joblib.load(models_path / 'club_encoding_fifa.joblib')
        print("   ✅ Modelo, encoder y club_encoding cargados")
    except FileNotFoundError as e:
        print(f"   ❌ Error: No se encontraron archivos del modelo: {e}")
        print("   💡 Ejecuta primero el entrenamiento del modelo")
        return None
    
    # 3. Configurar características (igual que en preprocesamiento_modelo.py)
    col_categoricas = [
        "categoria_posicion",
        "categoria_edad",
        "pie_preferido",
        "categoria_reputacion",
        "liga"
    ]
    
    col_numericas = [
        # TOP FEATURES
        "reputacion_internacional",
        "valoracion_global",
        "potencial",
        "movimiento_reacciones",
        
        # FEATURES MODERADAS
        "calidad_promedio",
        "pase",
        "mentalidad_compostura",
        "regate_gambeta",
        "mentalidad_vision",
        "tiro_disparo",
        "ataque_pase_corto",
        
        # ATAQUE
        "ataque_definicion",
        "ataque_cabezazo",
        "ataque_centros",
        "ataque_voleas",
        
        # FÍSICO
        "movimiento_velocidad_sprint",
        "movimiento_aceleracion",
        "movimiento_agilidad",
        "movimiento_equilibrio",
        "fisico",
        
        # DEFENSA
        "defensa",
        "defensa_entrada_pie",
        "defensa_entrada_deslizante",
        "defensa_marcaje",
        
        # MENTAL
        "mentalidad_agresividad",
        "mentalidad_intercepciones",
        "mentalidad_posicionamiento",
        "mentalidad_penales",
        
        # HABILIDADES
        "pie_debil",
        "habilidades_regate",
        "habilidad_regate",
        "habilidad_control_balon",
        "habilidad_efecto",
        "habilidad_pase_largo",
        "habilidad_tiros_libres",
        
        # FEATURES CALCULADAS
        "diferencia_potencial",
        "ratio_valor_salario",
        "anos_contrato_restantes",
        
        # DEMOGRAFÍA
        "edad"
    ]
    
    # Verificar columnas disponibles
    col_numericas_disponibles = [col for col in col_numericas if col in df_jugadores.columns]
    col_categoricas_disponibles = [col for col in col_categoricas if col in df_jugadores.columns]
    
    print(f"   📊 Columnas numéricas: {len(col_numericas_disponibles)}/{len(col_numericas)}")
    print(f"   📊 Columnas categóricas: {len(col_categoricas_disponibles)}/{len(col_categoricas)}")
    
    # 4. Procesar por año para mantener contexto temporal
    print("\n🔄 Generando predicciones por año...")
    resultados = []
    
    años_unicos = sorted(df_jugadores['año_datos'].unique())
    
    for año in años_unicos:
        print(f"\n   📅 Procesando año {año}...")
        
        df_año = df_jugadores[df_jugadores['año_datos'] == año].copy()
        print(f"      Jugadores: {len(df_año):,}")
        
        # Preparar datos (IGUAL que preprocesamiento_modelo.py)
        
        # 1. Separar categóricas y numéricas
        X_categoricas = df_año[col_categoricas_disponibles].copy()
        X_numericas = df_año[col_numericas_disponibles].copy()
        
        # 2. Target encoding para club usando club_encoding
        if 'club' in df_año.columns:
            X_numericas['club_valor_promedio'] = df_año['club'].map(club_encoding)
            # Si hay clubes nuevos, rellenar con mediana del dataset
            mediana_valor = df_año['valor_mercado_eur'].median()
            X_numericas['club_valor_promedio'].fillna(mediana_valor, inplace=True)
        
        # 3. Rellenar valores faltantes en numéricas
        X_numericas = X_numericas.fillna(X_numericas.median())
        
        # 4. OneHotEncoding para categóricas
        X_cat_encoded = encoder.transform(X_categoricas)
        
        # 5. Concatenar matrices numéricas y categóricas codificadas
        X_final = np.hstack([X_numericas.values, X_cat_encoded])
        
        # Transformar y predecir
        try:
            # IMPORTANTE: El modelo fue entrenado con log1p(valor), hay que revertir
            predicciones_log = modelo.predict(X_final)
            predicciones = np.expm1(predicciones_log)  # Revertir transformación log1p
            
            # Calcular diferencia porcentual
            df_año['valor_predicho_eur'] = predicciones
            
            # Evitar división por cero
            df_año['diferencia_porcentual'] = np.where(
                df_año['valor_mercado_eur'] > 0,
                ((df_año['valor_predicho_eur'] - df_año['valor_mercado_eur']) 
                 / df_año['valor_mercado_eur'] * 100),
                0
            )
            
            # Clasificar según tolerancia
            def clasificar(diff):
                if diff > tolerancia_porcentaje:
                    return 'I'  # Infravalorado
                elif diff < -tolerancia_porcentaje:
                    return 'S'  # Sobrevalorado
                else:
                    return 'J'  # Justo
            
            df_año['clasificacion_ml'] = df_año['diferencia_porcentual'].apply(clasificar)
            
            # Guardar solo columnas necesarias
            df_resultado = df_año[[
                'id_sofifa',
                'año_datos',
                'valor_mercado_eur',
                'valor_predicho_eur',
                'diferencia_porcentual',
                'clasificacion_ml'
            ]].copy()
            
            resultados.append(df_resultado)
            
            # Estadísticas del año
            total_i = (df_resultado['clasificacion_ml'] == 'I').sum()
            total_s = (df_resultado['clasificacion_ml'] == 'S').sum()
            total_j = (df_resultado['clasificacion_ml'] == 'J').sum()
            
            print(f"      💎 Infravalorados: {total_i:,}")
            print(f"      ⚠️ Sobrevalorados: {total_s:,}")
            print(f"      ✓ Justos: {total_j:,}")
            
        except Exception as e:
            print(f"      ❌ Error procesando año {año}: {e}")
            continue
    
    # 5. Concatenar todos los años
    print("\n📦 Consolidando resultados...")
    df_final = pd.concat(resultados, ignore_index=True)
    
    # 6. Agregar metadata
    df_final['tolerancia_porcentaje'] = tolerancia_porcentaje
    df_final['fecha_generacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 7. Guardar CSV
    output_path = data_path / 'jugadores_predicciones_ml.csv'
    df_final.to_csv(output_path, index=False)
    
    print("\n" + "="*70)
    print("✅ PREDICCIONES ML GENERADAS EXITOSAMENTE")
    print("="*70)
    print(f"📁 Archivo: {output_path}")
    print(f"📊 Total registros: {len(df_final):,}")
    print(f"\n📈 Distribución:")
    print(f"   💎 Infravalorados: {(df_final['clasificacion_ml']=='I').sum():,} ({(df_final['clasificacion_ml']=='I').sum()/len(df_final)*100:.1f}%)")
    print(f"   ⚠️ Sobrevalorados: {(df_final['clasificacion_ml']=='S').sum():,} ({(df_final['clasificacion_ml']=='S').sum()/len(df_final)*100:.1f}%)")
    print(f"   ✓ Justos: {(df_final['clasificacion_ml']=='J').sum():,} ({(df_final['clasificacion_ml']=='J').sum()/len(df_final)*100:.1f}%)")
    print(f"\n🎯 Tolerancia utilizada: {tolerancia_porcentaje}%")
    print("="*70)
    
    return df_final


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generar predicciones ML para todos los jugadores')
    parser.add_argument(
        '--tolerancia',
        type=float,
        default=8.0,
        help='Porcentaje de tolerancia para clasificación (default: 8.0)'
    )
    
    args = parser.parse_args()
    
    generar_predicciones_ml(tolerancia_porcentaje=args.tolerancia)
