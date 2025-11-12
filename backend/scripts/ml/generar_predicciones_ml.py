"""
Script para AGREGAR COLUMNAS ML a fifa_limpio.csv
Pre-calcula predicciones para todos los jugadores (122,501 registros)
Columnas agregadas: valor_predicho_eur, diferencia_porcentual, clasificacion_ml, tolerancia_porcentaje
"""

import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import os

# Obtener la ruta base del proyecto (3 niveles arriba desde este archivo)
BASE_DIR = Path(__file__).parent.parent.parent.parent  # backend/scripts/ml/ -> backend/ -> proyecto/
sys.path.append(str(BASE_DIR))

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
    data_path = BASE_DIR / 'datos' / 'procesados'
    models_path = BASE_DIR / 'datos' / 'modelos'
    
    # 1. Cargar dataset limpio
    print("\n📂 Cargando dataset...")
    csv_path = data_path / 'fifa_limpio.csv'
    if not csv_path.exists():
        print(f"   ❌ Error: No se encontró {csv_path}")
        return None
        
    df_jugadores = pd.read_csv(csv_path, low_memory=False)
    print(f"   ✅ Cargados {len(df_jugadores):,} registros × {len(df_jugadores.columns)} columnas")
    
    # 2. Cargar modelo, encoder y club_encoding
    print("\n🤖 Cargando componentes ML...")
    try:
        modelo_path = models_path / 'modelo_fifa.joblib'
        encoder_path = models_path / 'encoder_fifa.joblib'
        club_encoding_path = models_path / 'club_encoding_fifa.joblib'
        
        if not all([modelo_path.exists(), encoder_path.exists(), club_encoding_path.exists()]):
            print(f"   ❌ Error: Faltan archivos del modelo en {models_path}")
            print("   💡 Ejecuta primero: python backend/entrenamiento.py")
            return None
            
        modelo = joblib.load(modelo_path)
        encoder = joblib.load(encoder_path)
        club_encoding = joblib.load(club_encoding_path)
        print("   ✅ Modelo, encoder y club_encoding cargados")
    except Exception as e:
        print(f"   ❌ Error cargando modelo: {e}")
        return None
    
    # 3. Preparar columnas necesarias (exactamente como en preprocesamiento_modelo.py)
    print("\n🔄 Preparando características ML...")
    
    col_numericas = [
        "reputacion_internacional", "valoracion_global", "potencial", "movimiento_reacciones",
        "calidad_promedio", "pase", "mentalidad_compostura", "regate_gambeta",
        "mentalidad_vision", "tiro_disparo", "ataque_pase_corto", "ataque_definicion",
        "ataque_cabezazo", "ataque_centros", "ataque_voleas", "movimiento_velocidad_sprint",
        "movimiento_aceleracion", "movimiento_agilidad", "movimiento_equilibrio", "fisico",
        "defensa", "defensa_entrada_pie", "defensa_entrada_deslizante", "defensa_marcaje",
        "mentalidad_agresividad", "mentalidad_intercepciones", "mentalidad_posicionamiento",
        "mentalidad_penales", "pie_debil", "habilidades_regate", "habilidad_regate",
        "habilidad_control_balon", "habilidad_efecto", "habilidad_pase_largo",
        "habilidad_tiros_libres", "diferencia_potencial", "ratio_valor_salario",
        "anos_contrato_restantes", "edad"
    ]
    
    col_categoricas = [
        "categoria_posicion", "categoria_edad", "pie_preferido", 
        "categoria_reputacion", "liga"
    ]
    
    # Verificar columnas disponibles
    col_numericas_disponibles = [col for col in col_numericas if col in df_jugadores.columns]
    col_categoricas_disponibles = [col for col in col_categoricas if col in df_jugadores.columns]
    
    print(f"   📊 Numéricas: {len(col_numericas_disponibles)}/{len(col_numericas)}")
    print(f"   📊 Categóricas: {len(col_categoricas_disponibles)}/{len(col_categoricas)}")
    
    # 4. Aplicar Target Encoding para club
    print("\n🏟️  Aplicando Target Encoding para club...")
    # Usar club_encoding cargado desde el archivo
    df_jugadores['club_valor_promedio'] = df_jugadores['club'].map(club_encoding)
    df_jugadores['club_valor_promedio'].fillna(club_encoding.mean(), inplace=True)
    
    # Agregar club_valor_promedio a las columnas numéricas
    col_numericas_disponibles.append('club_valor_promedio')
    
    # 5. Extraer X numéricas y categóricas
    print("\n� Extrayendo features...")
    X_numericas = df_jugadores[col_numericas_disponibles].fillna(0)
    X_categoricas = df_jugadores[col_categoricas_disponibles].fillna('Desconocido')
    
    # 6. Transformar categóricas con encoder
    print("\n🔄 Aplicando OneHotEncoding...")
    X_categoricas_encoded = encoder.transform(X_categoricas)
    
    # Verificar si es sparse matrix o array
    if hasattr(X_categoricas_encoded, 'toarray'):
        X_categoricas_dense = X_categoricas_encoded.toarray()
    else:
        X_categoricas_dense = X_categoricas_encoded
    
    # 7. Concatenar numéricas + categóricas
    X_final = np.hstack([X_numericas.values, X_categoricas_dense])
    print(f"   ✅ Shape final: {X_final.shape}")
    
    # 8. Hacer predicciones
    print("\n🤖 Generando predicciones ML (esto puede tardar 1-2 minutos)...")
    try:
        predicciones_log = modelo.predict(X_final)
        predicciones_eur = np.expm1(predicciones_log)  # Revertir log1p
        
        print(f"   ✅ Predicciones generadas: {len(predicciones_eur):,}")
        
    except Exception as e:
        print(f"   ❌ Error en predicción: {e}")
        return None
    
    # 9. Calcular diferencia porcentual y clasificar
    print("\n📊 Calculando diferencias y clasificando...")
    
    # Evitar división por cero
    diferencias_porcentuales = np.where(
        df_jugadores['valor_predicho_eur'] > 0,
        ((predicciones_eur - df_jugadores['valor_mercado_eur']) 
         / predicciones_eur * 100),
        0
    )
    
    # Clasificar según tolerancia
    def clasificar(diff):
        if diff > tolerancia_porcentaje:
            return 'INFRAVALORADO'
        elif diff < -tolerancia_porcentaje:
            return 'SOBREVALORADO'
        else:
            return 'JUSTO'
    
    clasificaciones = [clasificar(d) for d in diferencias_porcentuales]
    
    # 10. Agregar columnas al DataFrame original
    print("\n➕ Agregando columnas ML al dataset...")
    df_jugadores['valor_predicho_eur'] = predicciones_eur
    df_jugadores['diferencia_porcentual'] = diferencias_porcentuales
    df_jugadores['clasificacion_ml'] = clasificaciones
    df_jugadores['tolerancia_porcentaje'] = tolerancia_porcentaje
    
    # Estadísticas
    total_i = (df_jugadores['clasificacion_ml'] == 'INFRAVALORADO').sum()
    total_s = (df_jugadores['clasificacion_ml'] == 'SOBREVALORADO').sum()
    total_j = (df_jugadores['clasificacion_ml'] == 'JUSTO').sum()
    
    print(f"   💎 Infravalorados: {total_i:,} ({total_i/len(df_jugadores)*100:.1f}%)")
    print(f"   ⚠️ Sobrevalorados: {total_s:,} ({total_s/len(df_jugadores)*100:.1f}%)")
    print(f"   ✓ Justos: {total_j:,} ({total_j/len(df_jugadores)*100:.1f}%)")
    
    # 11. Guardar CSV actualizado con backup
    print("\n� Guardando fifa_limpio.csv actualizado...")
    
    # Crear backup del archivo original (sin columnas ML)
    backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = data_path / f'fifa_limpio_backup_{backup_timestamp}.csv'
    
    # Leer CSV original para backup (sin las columnas nuevas)
    df_original = pd.read_csv(csv_path, low_memory=False)
    df_original.to_csv(backup_path, index=False)
    print(f"   ✅ Backup creado: {backup_path.name}")
    
    # Guardar dataset actualizado con columnas ML
    output_path = data_path / 'fifa_limpio.csv'
    df_jugadores.to_csv(output_path, index=False)
    
    print("\n" + "="*70)
    print("✅ COLUMNAS ML AGREGADAS EXITOSAMENTE A fifa_limpio.csv")
    print("="*70)
    print(f"📁 Archivo: {output_path}")
    print(f"📊 Registros: {len(df_jugadores):,}")
    print(f"📊 Columnas totales: {len(df_jugadores.columns)}")
    print(f"\n📊 Columnas ML agregadas:")
    print(f"   • valor_predicho_eur")
    print(f"   • diferencia_porcentual")
    print(f"   • clasificacion_ml")
    print(f"   • tolerancia_porcentaje")
    print(f"\n📈 Distribución de clasificaciones:")
    print(f"   💎 Infravalorados: {total_i:,} ({total_i/len(df_jugadores)*100:.1f}%)")
    print(f"   ⚠️ Sobrevalorados: {total_s:,} ({total_s/len(df_jugadores)*100:.1f}%)")
    print(f"   ✓ Justos: {total_j:,} ({total_j/len(df_jugadores)*100:.1f}%)")
    print(f"\n🎯 Tolerancia: {tolerancia_porcentaje}%")
    print(f"💾 Backup: {backup_path.name}")
    print("="*70)
    
    return df_jugadores


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
