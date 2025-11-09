"""
Módulo de Renombrado de Columnas
Sistema de Scouting FIFA

Traduce todas las columnas de inglés a español con nombres descriptivos.
"""

import pandas as pd


def renombrar_columnas_espanol(df):
   """
   Renombra todas las columnas de inglés a español con nombres descriptivos.
   Las siglas se expanden: 'GK' → 'gk_portero'
   
   Args:
   df: DataFrame con columnas en inglés
   
   Returns:
   DataFrame con columnas en español
   """
   print("\n" + "-"*60)
   print(" RENOMBRANDO COLUMNAS A ESPAÑOL")
   print("-"*60)
   
   # Diccionario completo de traducción
   renombres = {
   # Información de identificación y URLs
   'sofifa_id': 'id_sofifa',  #  ID único para referencia
   'player_url': 'url_jugador',  #  URL de SoFIFA (info + foto)
   'real_face': 'tiene_foto_real',  #  Indica si tiene foto real
   
   # Información básica
   'short_name': 'nombre_corto',
   'long_name': 'nombre_completo',
   'age': 'edad',
   'dob': 'fecha_nacimiento',
   'height_cm': 'altura_cm',
   'weight_kg': 'peso_kg',
   'nationality': 'nacionalidad',  #  Corregido: era 'nationality_name'
   'club_name': 'club',
   'league_name': 'liga',
   'player_positions': 'posiciones_jugador',
   'preferred_foot': 'pie_preferido',
   'body_type': 'tipo_cuerpo',
   'work_rate': 'ritmo_trabajo',
   
   # Valoración general
   'overall': 'valoracion_global',
   'potential': 'potencial',
   'value_eur': 'valor_mercado_eur',
   'wage_eur': 'salario_eur',
   'release_clause_eur': 'clausula_rescision_eur',
   'international_reputation': 'reputacion_internacional',
   'contract_valid_until': 'contrato_valido_hasta',
   
   # Habilidades especiales
   'weak_foot': 'pie_debil',
   'skill_moves': 'habilidades_regate',
   
   # Atributos principales (6 categorías FIFA)
   'pace': 'ritmo_velocidad',
   'shooting': 'tiro_disparo',
   'passing': 'pase',
   'dribbling': 'regate_gambeta',
   'defending': 'defensa',
   'physic': 'fisico',
   
   # Atributos de ataque
   'attacking_crossing': 'ataque_centros',
   'attacking_finishing': 'ataque_definicion',
   'attacking_heading_accuracy': 'ataque_cabezazo',
   'attacking_short_passing': 'ataque_pase_corto',
   'attacking_volleys': 'ataque_voleas',
   
   # Atributos de habilidad/técnica
   'skill_dribbling': 'habilidad_regate',
   'skill_curve': 'habilidad_efecto',
   'skill_fk_accuracy': 'habilidad_tiros_libres',
   'skill_long_passing': 'habilidad_pase_largo',
   'skill_ball_control': 'habilidad_control_balon',
   
   # Atributos de movimiento
   'movement_acceleration': 'movimiento_aceleracion',
   'movement_sprint_speed': 'movimiento_velocidad_sprint',
   'movement_agility': 'movimiento_agilidad',
   'movement_reactions': 'movimiento_reacciones',
   'movement_balance': 'movimiento_equilibrio',
   
   # Atributos de potencia
   'power_shot_power': 'potencia_disparo',
   'power_jumping': 'potencia_salto',
   'power_stamina': 'potencia_resistencia',
   'power_strength': 'potencia_fuerza',
   'power_long_shots': 'potencia_tiros_lejanos',
   
   # Atributos mentales
   'mentality_aggression': 'mentalidad_agresividad',
   'mentality_interceptions': 'mentalidad_intercepciones',
   'mentality_positioning': 'mentalidad_posicionamiento',
   'mentality_vision': 'mentalidad_vision',
   'mentality_penalties': 'mentalidad_penales',
   'mentality_composure': 'mentalidad_compostura',
   
   # Atributos de defensa
   'defending_marking': 'defensa_marcaje',  #  Corregido: era 'defending_marking_awareness'
   'defending_standing_tackle': 'defensa_entrada_pie',
   'defending_sliding_tackle': 'defensa_entrada_deslizante',
   
   # Atributos de portero (GK = Goalkeeper)
   'goalkeeping_diving': 'gk_portero_estirada',
   'goalkeeping_handling': 'gk_portero_manejo',
   'goalkeeping_kicking': 'gk_portero_saque',
   'goalkeeping_positioning': 'gk_portero_colocacion',
   'goalkeeping_reflexes': 'gk_portero_reflejos',
   
   # Columna de año (si existe)
   'año_datos': 'año_datos'  # Ya está en español
   }
   
   # Aplicar renombrado
   columnas_antes = df.columns.tolist()
   df_renombrado = df.rename(columns=renombres)
   columnas_despues = df_renombrado.columns.tolist()
   
   # Contar cuántas se renombraron
   columnas_renombradas = [col for col in columnas_antes if col in renombres]
   columnas_sin_renombrar = [col for col in columnas_antes if col not in renombres]
   
   print(f"  Columnas totales: {len(columnas_antes)}")
   print(f"  Columnas renombradas: {len(columnas_renombradas)}")
   
   if columnas_sin_renombrar:
       print(f"  Columnas sin renombrar: {len(columnas_sin_renombrar)}")
       if len(columnas_sin_renombrar) <= 10:
           print(f"\n     Columnas que quedaron sin renombrar:")
           for col in columnas_sin_renombrar:
               print(f"   {col}")
   
   # Mostrar algunos ejemplos de renombrado
   print(f"\n   Ejemplos de renombrado:")
   ejemplos = list(renombres.items())[:5]
   for original, nuevo in ejemplos:
       if original in columnas_antes:
           print(f"   {original} → {nuevo}")
   
   print(f"\n   Renombrado completado")
   print("-"*60)
   
   return df_renombrado


def convertir_columnas_minusculas(df):
   """
   Convierte todos los nombres de columnas a minúsculas (opcional).
   
   Args:
   df: DataFrame
   
   Returns:
   DataFrame con columnas en minúsculas
   """
   print("\n" + "-"*60)
   print(" CONVIRTIENDO COLUMNAS A MINÚSCULAS")
   print("-"*60)
   
   df_lower = df.copy()
   df_lower.columns = df_lower.columns.str.lower()
   
   print(f"   Todas las columnas convertidas a minúsculas")
   print("-"*60)
   
   return df_lower
