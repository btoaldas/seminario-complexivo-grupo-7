"""
Script para optimizar el dataset FIFA para carga rápida en el API
Convierte CSV a Parquet (10x más rápido) y optimiza tipos de datos
"""

import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_PATH = BASE_DIR / 'datos' / 'procesados'

def optimizar_dataset():
    """
    Convierte fifa_limpio.csv a Parquet optimizado
    Reduce tiempo de carga de ~20s a ~2-3s
    """
    print("="*70)
    print("⚡ OPTIMIZADOR DE DATASET FIFA")
    print("="*70)
    
    csv_path = DATA_PATH / 'fifa_limpio.csv'
    parquet_path = DATA_PATH / 'fifa_limpio.parquet'
    
    if not csv_path.exists():
        print(f"❌ Error: No se encontró {csv_path}")
        return
    
    # 1. Cargar CSV
    print(f"\n📂 Cargando {csv_path.name}...")
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"   ✅ Cargado: {len(df):,} registros × {len(df.columns)} columnas")
    
    # 2. Optimizar tipos de datos
    print("\n🔧 Optimizando tipos de datos...")
    
    # Columnas categóricas (strings repetitivos)
    categoricas = [
        'club', 'liga', 'nacionalidad', 'posiciones_jugador', 
        'pie_preferido', 'categoria_posicion', 'categoria_edad',
        'categoria_reputacion', 'clasificacion_ml'
    ]
    
    for col in categoricas:
        if col in df.columns:
            df[col] = df[col].astype('category')
            print(f"   • {col} → category")
    
    # Columnas int (ahorrar memoria)
    int_cols = [
        'edad', 'valoracion_global', 'potencial', 'altura_cm', 'peso_kg',
        'reputacion_internacional', 'pie_debil', 'año_datos'
    ]
    
    for col in int_cols:
        if col in df.columns and df[col].dtype == 'float64':
            df[col] = df[col].fillna(0).astype('int32')
            print(f"   • {col} → int32")
    
    # 3. Calcular tamaño antes/después
    csv_size_mb = csv_path.stat().st_size / (1024 * 1024)
    
    # 4. Guardar como Parquet
    print(f"\n💾 Guardando {parquet_path.name}...")
    df.to_parquet(
        parquet_path,
        engine='pyarrow',
        compression='snappy',
        index=False
    )
    
    parquet_size_mb = parquet_path.stat().st_size / (1024 * 1024)
    
    print("\n" + "="*70)
    print("✅ DATASET OPTIMIZADO EXITOSAMENTE")
    print("="*70)
    print(f"📁 Archivos generados:")
    print(f"   • CSV:     {csv_path.name} ({csv_size_mb:.1f} MB)")
    print(f"   • Parquet: {parquet_path.name} ({parquet_size_mb:.1f} MB)")
    print(f"\n📊 Reducción de tamaño: {((csv_size_mb - parquet_size_mb) / csv_size_mb * 100):.1f}%")
    print(f"⚡ Velocidad de carga estimada:")
    print(f"   • CSV:     ~15-20 segundos")
    print(f"   • Parquet: ~2-3 segundos (7x más rápido)")
    print("="*70)
    
    return df


if __name__ == "__main__":
    optimizar_dataset()
