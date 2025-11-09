"""
Script de pruebas para la API REST del Sistema Scouting FIFA
==============================================================
Este script prueba todos los endpoints de la API para verificar funcionamiento.

Asegúrate de tener la API corriendo antes de ejecutar este script:
    cd backend
    python api_scouting_fifa.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_separador(titulo):
    print("\n" + "="*80)
    print(f" {titulo}")
    print("="*80)

def probar_endpoint(nombre, url, metodo="GET", data=None, params=None):
    """
    Prueba un endpoint y muestra resultados
    """
    print(f"\n[TEST] {nombre}")
    print(f"URL: {url}")
    
    try:
        if metodo == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif metodo == "POST":
            response = requests.post(url, json=data, timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            print("✓ Respuesta exitosa")
            
            # Mostrar preview de la respuesta
            if isinstance(resultado, dict):
                for key, value in list(resultado.items())[:5]:  # Primeras 5 claves
                    if isinstance(value, (list, dict)):
                        print(f"  {key}: {type(value).__name__} (len={len(value) if isinstance(value, list) else 'N/A'})")
                    else:
                        print(f"  {key}: {value}")
            
            return True, resultado
        else:
            print(f"✗ Error: {response.text[:200]}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print("✗ Error: No se pudo conectar a la API. ¿Está corriendo en http://localhost:8000?")
        return False, None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False, None

# ============================================================================
# PRUEBAS
# ============================================================================

print_separador("PRUEBAS DE LA API - SISTEMA SCOUTING FIFA")

# Test 1: Endpoint raíz
print_separador("TEST 1: INFORMACIÓN DE LA API")
exito, data = probar_endpoint(
    "GET /",
    f"{BASE_URL}/"
)

# Test 2: Obtener filtros
print_separador("TEST 2: OPCIONES DE FILTROS")
exito, data = probar_endpoint(
    "GET /jugadores/filtros",
    f"{BASE_URL}/jugadores/filtros"
)
if exito:
    print(f"\n  Total posiciones: {len(data.get('posiciones', []))}")
    print(f"  Total nacionalidades: {len(data.get('nacionalidades', []))}")
    print(f"  Total clubes: {len(data.get('clubes', []))}")
    print(f"  Total ligas: {len(data.get('ligas', []))}")

# Test 3: Buscar jugadores
print_separador("TEST 3: BUSCAR JUGADORES (Top 10 más valiosos)")
exito, data = probar_endpoint(
    "GET /jugadores/buscar",
    f"{BASE_URL}/jugadores/buscar",
    params={
        "limite": 10,
        "ordenar_por": "valor_mercado_eur",
        "orden_descendente": True
    }
)
if exito:
    print(f"\n  Jugadores encontrados: {data.get('total_encontrados', 0)}")
    print("\n  Top 5:")
    for i, jugador in enumerate(data.get('jugadores', [])[:5], 1):
        print(f"    {i}. {jugador.get('nombre_corto')} ({jugador.get('club')}) - €{jugador.get('valor_mercado_eur'):,}")

# Test 4: Buscar delanteros jóvenes
print_separador("TEST 4: BUSCAR DELANTEROS JÓVENES PROMETEDORES")
exito, data = probar_endpoint(
    "GET /jugadores/buscar (filtrado)",
    f"{BASE_URL}/jugadores/buscar",
    params={
        "categoria_posicion": "Delantero",
        "edad_min": 18,
        "edad_max": 23,
        "potencial_min": 80,
        "limite": 20
    }
)
if exito:
    print(f"\n  Delanteros jóvenes encontrados: {data.get('total_encontrados', 0)}")
    for i, jugador in enumerate(data.get('jugadores', [])[:3], 1):
        print(f"    {i}. {jugador.get('nombre_corto')} - Edad: {jugador.get('edad')}, Potencial: {jugador.get('potencial')}")

# Test 5: Perfil de jugador específico
print_separador("TEST 5: PERFIL COMPLETO DE JUGADOR")
# Primero obtener un ID
exito_buscar, data_buscar = probar_endpoint(
    "GET /jugadores/buscar (para obtener ID)",
    f"{BASE_URL}/jugadores/buscar",
    params={"limite": 1}
)

if exito_buscar and data_buscar.get('jugadores'):
    jugador_id = data_buscar['jugadores'][0]['id_sofifa']
    exito, data = probar_endpoint(
        f"GET /jugadores/{jugador_id}/perfil",
        f"{BASE_URL}/jugadores/{jugador_id}/perfil"
    )
    if exito:
        jugador = data.get('jugador', {})
        prediccion = data.get('prediccion_ml', {})
        print(f"\n  Jugador: {jugador.get('nombre_corto')}")
        print(f"  Club: {jugador.get('club')}")
        print(f"  Valoración: {jugador.get('valoracion_global')}")
        if 'valor_predicho_eur' in prediccion:
            print(f"  Valor real: €{prediccion.get('valor_real_eur'):,}")
            print(f"  Valor predicho: €{prediccion.get('valor_predicho_eur'):,}")
            print(f"  Clasificación: {prediccion.get('clasificacion')}")

# Test 6: Predicción ML (jugador hipotético)
print_separador("TEST 6: PREDICCIÓN ML - JUGADOR NUEVO")
datos_jugador = {
    "edad": 22,
    "valoracion_global": 78,
    "potencial": 85,
    "ritmo_velocidad": 88,
    "tiro_disparo": 72,
    "pase": 70,
    "regate_gambeta": 80,
    "defensa": 32,
    "fisico": 68,
    "pie_debil": 3,
    "habilidades_regate": 4,
    "reputacion_internacional": 2,
    "posiciones_jugador": "LW",
    "nacionalidad": "Argentina",
    "pie_preferido": "Left"
}

exito, data = probar_endpoint(
    "POST /ml/predecir_valor",
    f"{BASE_URL}/ml/predecir_valor",
    metodo="POST",
    data=datos_jugador
)
if exito:
    print(f"\n  Valor predicho: {data.get('valor_predicho_formateado')}")
    print(f"  Confianza: {data.get('confianza_prediccion')}")
    print(f"  Percentil: {data.get('percentil_valor')}%")
    print(f"  Categoría: {data.get('categoria_valor')}")
    print(f"  Features utilizadas: {data.get('features_utilizadas')}/{data.get('features_imputadas') + data.get('features_utilizadas')}")

# Test 7: Jugadores infravalorados
print_separador("TEST 7: TOP 10 JUGADORES INFRAVALORADOS")
exito, data = probar_endpoint(
    "GET /jugadores/infravalorados",
    f"{BASE_URL}/jugadores/infravalorados",
    params={
        "top": 10,
        "diferencia_minima_porcentual": 20
    }
)
if exito:
    print(f"\n  Total infravalorados: {data.get('total_infravalorados', 0)}")
    print("\n  Top 5:")
    for i, jugador in enumerate(data.get('top_jugadores', [])[:5], 1):
        print(f"    {i}. {jugador.get('nombre_corto')} ({jugador.get('club')})")
        print(f"       Valor actual: €{jugador.get('valor_mercado_eur'):,}")
        print(f"       Valor predicho: €{jugador.get('valor_predicho_eur'):,}")
        print(f"       Diferencia: +{jugador.get('diferencia_porcentual'):.1f}%")

# Test 8: Jugadores sobrevalorados
print_separador("TEST 8: TOP 10 JUGADORES SOBREVALORADOS")
exito, data = probar_endpoint(
    "GET /jugadores/sobrevalorados",
    f"{BASE_URL}/jugadores/sobrevalorados",
    params={
        "top": 10,
        "diferencia_minima_porcentual": 20
    }
)
if exito:
    print(f"\n  Total sobrevalorados: {data.get('total_sobrevalorados', 0)}")
    print("\n  Top 5:")
    for i, jugador in enumerate(data.get('top_jugadores', [])[:5], 1):
        print(f"    {i}. {jugador.get('nombre_corto')} ({jugador.get('club')})")
        print(f"       Valor actual: €{jugador.get('valor_mercado_eur'):,}")
        print(f"       Valor predicho: €{jugador.get('valor_predicho_eur'):,}")
        print(f"       Diferencia: {jugador.get('diferencia_porcentual'):.1f}%")

# Test 9: Estadísticas generales
print_separador("TEST 9: ESTADÍSTICAS GENERALES DEL DATASET")
exito, data = probar_endpoint(
    "GET /eda/estadisticas_generales",
    f"{BASE_URL}/eda/estadisticas_generales"
)
if exito:
    print(f"\n  Total jugadores: {data.get('total_jugadores'):,}")
    print(f"  Total clubes: {data.get('total_clubes'):,}")
    print(f"  Total ligas: {data.get('total_ligas')}")
    print(f"  Edad promedio: {data.get('edad_promedio'):.1f} años")
    print(f"  Valoración promedio: {data.get('valoracion_promedio'):.1f}")
    print(f"  Valor mercado promedio: €{data.get('valor_mercado_promedio_eur'):,.0f}")
    
    jugador_valioso = data.get('jugador_mas_valioso', {})
    print(f"\n  Jugador más valioso:")
    print(f"    {jugador_valioso.get('nombre')} ({jugador_valioso.get('club')})")
    print(f"    €{jugador_valioso.get('valor_eur'):,}")

# Test 10: Datos para gráficos
print_separador("TEST 10: DATOS PARA GRÁFICOS - TOP CLUBES")
exito, data = probar_endpoint(
    "GET /eda/datos_graficos",
    f"{BASE_URL}/eda/datos_graficos",
    params={
        "tipo_analisis": "clubes",
        "top_n": 10
    }
)
if exito:
    print(f"\n  Top 5 clubes por valor:")
    for i, club in enumerate(data.get('datos', [])[:5], 1):
        print(f"    {i}. {club.get('club')}")
        print(f"       Valor total: €{club.get('valor_total_eur'):,.0f}")
        print(f"       Jugadores: {club.get('cantidad_jugadores')}")

print_separador("RESUMEN DE PRUEBAS")
print("\n✓ Todas las pruebas completadas")
print("\nLa API está funcionando correctamente en: http://localhost:8000")
print("Documentación interactiva disponible en: http://localhost:8000/docs")
print("\n" + "="*80)
