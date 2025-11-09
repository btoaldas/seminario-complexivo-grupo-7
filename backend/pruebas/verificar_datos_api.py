"""
Script para verificar las columnas y valores únicos del dataset
para construir la API correctamente
"""
import pandas as pd

df = pd.read_csv('../datos/fifa_limpio.csv')

print('='*80)
print('INFORMACIÓN CLAVE PARA CONSTRUCCIÓN DE LA API')
print('='*80)

print(f'\nTotal jugadores: {len(df):,}')

print(f'\nPOSICIONES únicas ({df["posiciones_jugador"].nunique()}):')
print(sorted(df["posiciones_jugador"].unique())[:20])

print(f'\nNACIONALIDADES únicas ({df["nacionalidad"].nunique()}):')
print(sorted(df["nacionalidad"].unique())[:20])

print(f'\nCLUBS únicos ({df["club"].nunique()}):')
print(sorted(df["club"].unique())[:15])

print(f'\nLIGAS únicas ({df["liga"].nunique()}):')
print(sorted(df["liga"].unique()))

print(f'\nCATEGORIA_EDAD:')
print(sorted(df["categoria_edad"].unique()))

print(f'\nCATEGORIA_POSICION:')
print(sorted(df["categoria_posicion"].unique()))

print(f'\nCATEGORIA_REPUTACION:')
print(sorted(df["categoria_reputacion"].unique()))

print(f'\nPIE_PREFERIDO:')
print(sorted(df["pie_preferido"].unique()))

print(f'\nRITMO_TRABAJO (work_rate):')
print(sorted(df["ritmo_trabajo"].unique())[:10])

print(f'\nRANGOS NUMÉRICOS:')
print(f'  - Edad: {df["edad"].min()}-{df["edad"].max()} años')
print(f'  - Valoración: {df["valoracion_global"].min()}-{df["valoracion_global"].max()}')
print(f'  - Potencial: {df["potencial"].min()}-{df["potencial"].max()}')
print(f'  - Valor mercado: €{df["valor_mercado_eur"].min():,.0f} - €{df["valor_mercado_eur"].max():,.0f}')

print(f'\nATRIBUTOS TÉCNICOS (rangos):')
print(f'  - Ritmo: {df["ritmo_velocidad"].min()}-{df["ritmo_velocidad"].max()}')
print(f'  - Tiro: {df["tiro_disparo"].min()}-{df["tiro_disparo"].max()}')
print(f'  - Pase: {df["pase"].min()}-{df["pase"].max()}')
print(f'  - Regate: {df["regate_gambeta"].min()}-{df["regate_gambeta"].max()}')
print(f'  - Defensa: {df["defensa"].min()}-{df["defensa"].max()}')
print(f'  - Físico: {df["fisico"].min()}-{df["fisico"].max()}')

print(f'\nCOLUMNAS CON VALORES NULOS (importantes):')
nulos = df.isnull().sum()
nulos_importantes = nulos[nulos > 0].head(10)
for col, cant in nulos_importantes.items():
    print(f'  - {col}: {cant:,} ({cant/len(df)*100:.1f}%)')

print('\n' + '='*80)
print('VERIFICACIÓN COMPLETADA')
print('='*80)
