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
    base_path = Path(__file__).parent.parent.parent
    data_path = base_path / 'datos' / 'procesados'
    models_path = base_path / 'modelos'
    
    # 1. Cargar dataset limpio
    print("\n📂 Cargando dataset...")
    df_jugadores = pd.read_csv(data_path / 'fifa_limpio.csv')
    print(f"   ✅ Cargados {len(df_jugadores):,} registros")
    
    # 2. Cargar modelo y preprocesador
    print("\n🤖 Cargando modelo ML...")
    try:
        modelo = joblib.load(models_path / 'mejor_modelo_rf.pkl')
        preprocesador = joblib.load(models_path / 'preprocesador.pkl')
        print("   ✅ Modelo y preprocesador cargados")
    except FileNotFoundError as e:
        print(f"   ❌ Error: No se encontraron archivos del modelo: {e}")
        print("   💡 Ejecuta primero el entrenamiento del modelo")
        return None
    
    # 3. Características necesarias para predicción
    caracteristicas = [
        # Básicas
        'edad', 'valoracion_global', 'potencial', 'altura_cm', 'peso_kg',
        'reputacion_internacional', 'pie_debil', 'movimientos_habilidad',
        
        # Atributos principales
        'ritmo', 'tiro', 'pase', 'regate', 'defensa', 'fisico',
        
        # Ataque
        'ataque_cabezazo', 'ataque_definicion', 'ataque_potencia_disparo',
        'ataque_efecto', 'ataque_voleas', 'ataque_penales',
        
        # Habilidad
        'habilidad_regate', 'habilidad_control_balon', 'habilidad_aceleracion',
        'habilidad_velocidad_sprint', 'habilidad_agilidad', 'habilidad_reacciones',
        'habilidad_equilibrio',
        
        # Movimiento
        'movimiento_aceleracion', 'movimiento_velocidad_sprint', 'movimiento_agilidad',
        'movimiento_reacciones', 'movimiento_equilibrio',
        
        # Potencia
        'potencia_disparo', 'potencia_salto', 'potencia_stamina', 'potencia_fuerza',
        'potencia_disparo_lejano',
        
        # Mentalidad
        'mentalidad_agresividad', 'mentalidad_intercepciones', 'mentalidad_posicionamiento',
        'mentalidad_vision', 'mentalidad_penales', 'mentalidad_compostura',
        
        # Defensa
        'defensa_marca', 'defensa_parado', 'defensa_entrada_pie',
        
        # Portero
        'porteria_buceo', 'porteria_manejo', 'porteria_patada',
        'porteria_reflejos', 'porteria_velocidad', 'porteria_posicionamiento'
    ]
    
    # Verificar que todas las columnas existen
    caracteristicas_disponibles = [col for col in caracteristicas if col in df_jugadores.columns]
    print(f"   📊 Características disponibles: {len(caracteristicas_disponibles)}/{len(caracteristicas)}")
    
    # 4. Procesar por año para mantener contexto temporal
    print("\n🔄 Generando predicciones por año...")
    resultados = []
    
    años_unicos = sorted(df_jugadores['año_datos'].unique())
    
    for año in años_unicos:
        print(f"\n   📅 Procesando año {año}...")
        
        df_año = df_jugadores[df_jugadores['año_datos'] == año].copy()
        print(f"      Jugadores: {len(df_año):,}")
        
        # Preparar datos
        X = df_año[caracteristicas_disponibles].copy()
        
        # Rellenar valores faltantes
        X = X.fillna(X.median())
        
        # Transformar y predecir
        try:
            X_procesado = preprocesador.transform(X)
            predicciones = modelo.predict(X_procesado)
            
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
