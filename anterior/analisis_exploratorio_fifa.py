"""
Análisis exploratorio rápido del dataset FIFA limpio
Verifica calidad de datos y genera estadísticas descriptivas
"""

import pandas as pd
import numpy as np

print("="*70)
print("ANÁLISIS EXPLORATORIO - DATASET FIFA LIMPIO")
print("="*70)

# cargar dataset limpio
df = pd.read_csv("data/jugadores_fifa_limpio.csv")

print(f"\n[1] INFORMACIÓN GENERAL")
print(f"{'='*70}")
print(f"Dimensiones: {df.shape[0]:,} filas x {df.shape[1]} columnas")
print(f"Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print(f"\n[2] VALORES NULOS POR COLUMNA CLAVE")
print(f"{'='*70}")
columnas_clave = ['nombre', 'age', 'posicion', 'club', 'overall', 'potential', 
                  'valor_mercado', 'salario', 'anio']
for col in columnas_clave:
    nulos = df[col].isna().sum()
    porcentaje = (nulos / len(df)) * 100
    print(f"  {col:20s}: {nulos:6,} NaN ({porcentaje:5.2f}%)")

print(f"\n[3] DISTRIBUCIÓN POR AÑO")
print(f"{'='*70}")
print(df['anio'].value_counts().sort_index())
print(f"\nTotal registros: {len(df):,}")

print(f"\n[4] ESTADÍSTICAS NUMÉRICAS")
print(f"{'='*70}")
print(f"\nEdad:")
print(f"  Min: {df['age'].min()} años")
print(f"  Max: {df['age'].max()} años")
print(f"  Media: {df['age'].mean():.1f} años")
print(f"  Mediana: {df['age'].median():.1f} años")

print(f"\nOverall (Calificación General):")
print(f"  Min: {df['overall'].min()}")
print(f"  Max: {df['overall'].max()}")
print(f"  Media: {df['overall'].mean():.1f}")
print(f"  Mediana: {df['overall'].median():.1f}")

print(f"\nValor de Mercado (euros):")
print(f"  Min: €{df['valor_mercado'].min():,.0f}")
print(f"  Max: €{df['valor_mercado'].max():,.0f}")
print(f"  Media: €{df['valor_mercado'].mean():,.0f}")
print(f"  Mediana: €{df['valor_mercado'].median():,.0f}")

print(f"\nSalario Semanal (euros):")
print(f"  Min: €{df['salario'].min():,.0f}")
print(f"  Max: €{df['salario'].max():,.0f}")
print(f"  Media: €{df['salario'].mean():,.0f}")
print(f"  Mediana: €{df['salario'].median():,.0f}")

print(f"\n[5] TOP 10 JUGADORES POR OVERALL")
print(f"{'='*70}")
top_overall = df.nlargest(10, 'overall')[['nombre', 'age', 'overall', 'potential', 
                                           'posicion', 'club', 'valor_mercado', 'anio']]
print(top_overall.to_string(index=False))

print(f"\n[6] TOP 10 JUGADORES POR VALOR DE MERCADO")
print(f"{'='*70}")
top_valor = df.nlargest(10, 'valor_mercado')[['nombre', 'age', 'overall', 
                                               'valor_mercado', 'salario', 
                                               'club', 'anio']]
top_valor['valor_mercado'] = top_valor['valor_mercado'].apply(lambda x: f"€{x/1e6:.1f}M")
top_valor['salario'] = top_valor['salario'].apply(lambda x: f"€{x/1e3:.0f}k")
print(top_valor.to_string(index=False))

print(f"\n[7] TOP 10 CLUBES CON MÁS JUGADORES")
print(f"{'='*70}")
top_clubes = df['club'].value_counts().head(10)
for idx, (club, count) in enumerate(top_clubes.items(), 1):
    print(f"  {idx:2d}. {club:30s}: {count:4,} jugadores")

print(f"\n[8] DISTRIBUCIÓN DE POSICIONES")
print(f"{'='*70}")
# extraer primera posición (algunos jugadores tienen múltiples)
df['posicion_principal'] = df['posicion'].str.split(',').str[0].str.strip()
top_posiciones = df['posicion_principal'].value_counts().head(10)
for idx, (pos, count) in enumerate(top_posiciones.items(), 1):
    porcentaje = (count / len(df)) * 100
    print(f"  {idx:2d}. {pos:5s}: {count:6,} ({porcentaje:5.2f}%)")

print(f"\n[9] NACIONALIDADES MÁS REPRESENTADAS")
print(f"{'='*70}")
top_nacionalidades = df['nationality'].value_counts().head(10)
for idx, (pais, count) in enumerate(top_nacionalidades.items(), 1):
    print(f"  {idx:2d}. {pais:20s}: {count:4,} jugadores")

print(f"\n[10] ANÁLISIS DE POTENCIAL VS OVERALL")
print(f"{'='*70}")
df['margen_crecimiento'] = df['potential'] - df['overall']
print(f"Jugadores con potencial > overall: {(df['margen_crecimiento'] > 0).sum():,}")
print(f"Jugadores en su máximo: {(df['margen_crecimiento'] == 0).sum():,}")
print(f"Margen promedio de crecimiento: {df['margen_crecimiento'].mean():.2f} puntos")

# top 10 con mayor margen de crecimiento (jóvenes promesas)
print(f"\nTop 10 Jóvenes Promesas (mayor potencial - overall):")
promesas = df.nlargest(10, 'margen_crecimiento')[['nombre', 'age', 'overall', 
                                                    'potential', 'margen_crecimiento',
                                                    'club', 'anio']]
print(promesas.to_string(index=False))

print(f"\n[11] RESUMEN DE CALIDAD DE DATOS")
print(f"{'='*70}")
total_valores = df.size
valores_nulos = df.isna().sum().sum()
porcentaje_completo = ((total_valores - valores_nulos) / total_valores) * 100

print(f"Total de valores: {total_valores:,}")
print(f"Valores nulos: {valores_nulos:,}")
print(f"Completitud: {porcentaje_completo:.2f}%")

# verificar duplicados
duplicados = df.duplicated(subset=['sofifa_id', 'anio']).sum()
print(f"Duplicados (sofifa_id + anio): {duplicados}")

# verificar rangos válidos
edad_valida = ((df['age'] >= 15) & (df['age'] <= 45)).all()
overall_valido = ((df['overall'] >= 0) & (df['overall'] <= 100)).all()
potential_valido = ((df['potential'] >= 0) & (df['potential'] <= 100)).all()

print(f"\nValidaciones:")
print(f"  ✓ Edades válidas (15-45): {edad_valida}")
print(f"  ✓ Overall válido (0-100): {overall_valido}")
print(f"  ✓ Potential válido (0-100): {potential_valido}")

print(f"\n{'='*70}")
print("✓ ANÁLISIS COMPLETADO")
print(f"{'='*70}")
