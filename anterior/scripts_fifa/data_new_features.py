import pandas as pd

def  crear_ventas_totales(df):
    """
    crea una nueva columna 'ventas_totales' sumando las ventas de diferentes regiones.
    
    args:
        df: DataFrame con columnas de ventas por región
        
    returns:
        DataFrame con la nueva columna 'ventas_totales'
    """
    print("creando columna 'ventas_totales'...")
    regiones_ventas = ['ventas_norte_america', 'ventas_europa', 'ventas_japon', 'ventas_otras_regiones']
    df['ventas_totales'] = df[regiones_ventas].sum(axis=1)
    return df

def asignar_generacion(plataforma):
    """
    asigna la generación de consola basada en la plataforma.
    
    args:
        plataforma: nombre de la plataforma (ej: 'ps4', 'xbox one')
        
    returns:
        string con la generación de consola
    """
    generacion_map = {
        'ps2': 'sexta',
        'xbox': 'sexta',
        'gamecube': 'sexta',
        'ps3': 'séptima',
        'xbox 360': 'séptima',
        'wii': 'séptima',
        'ps4': 'octava',
        'xbox one': 'octava',
        'switch': 'octava'
    }
    return generacion_map.get(plataforma.lower(), 'desconocida')

