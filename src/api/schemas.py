from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, validator


class PosicionPrincipal(str, Enum):
    """
    Posiciones principales válidas según el dataset usado en el modelo.
    """

    CAM = "CAM"
    CB = "CB"
    CDM = "CDM"
    CF = "CF"
    CM = "CM"
    GK = "GK"
    LB = "LB"
    LM = "LM"
    LW = "LW"
    LWB = "LWB"
    RB = "RB"
    RM = "RM"
    RW = "RW"
    RWB = "RWB"
    ST = "ST"


class PiePreferido(str, Enum):
    """Valores de pie preferido presentes en el modelo (codificados como Left/Right)."""

    Left = "Left"
    Right = "Right"


class JugadorEntrada(BaseModel):
    """
    Entrada para predicción del valor de mercado.

    Incluye las variables necesarias para reproducir el preprocesamiento
    del cuaderno `modelo_ml.ipynb` (IMC y margen de crecimiento), además
    de las variables categóricas requeridas para el one-hot encoding.
    """

    # Datos opcionales de identidad (no afectan la inferencia)
    nombre_corto: Optional[str] = Field(
        None, description="Nombre corto del jugador (opcional)"
    )
    nombre_completo: Optional[str] = Field(
        None, description="Nombre completo del jugador (opcional)"
    )

    edad: int = Field(..., ge=14, le=50, description="Edad del jugador en años")
    calificacion_general: int = Field(
        ..., ge=1, le=99, description="Calificación general actual (OVR)"
    )
    potencial: int = Field(..., ge=1, le=99, description="Potencial máximo")
    altura_cm: float = Field(..., gt=0, description="Altura en centímetros")
    peso_kg: float = Field(..., gt=0, description="Peso en kilogramos")
    posicion_principal: PosicionPrincipal
    pie_preferido: PiePreferido
    id_jugador: Optional[str] = Field(
        None, description="ID opcional para correlacionar respuesta con la solicitud"
    )

    @validator("potencial")
    def validar_potencial_vs_calificacion(cls, v, values):
        """Asegura que el potencial no sea menor que la calificación actual."""
        calif = values.get("calificacion_general")
        if calif is not None and v < calif:
            raise ValueError("El potencial no puede ser menor que la calificación actual")
        return v


class PrediccionValor(BaseModel):
    """Respuesta de la API con el valor estimado."""

    id_jugador: Optional[str] = None
    valor_estimado: float = Field(..., description="Valor estimado en euros (€)")
    moneda: str = Field("EUR", description="Moneda de la predicción")
    modelo: str = Field(
        "RandomForestRegressor",
        description="Nombre del modelo entrenado para referencia",
    )
    # Campos opcionales para compatibilidad con vistas/UX
    valor_estimado_formateado: Optional[str] = Field(
        None, description="Valor estimado formateado (ej.: '€49.36M')"
    )
    nombre_corto: Optional[str] = None
    nombre_completo: Optional[str] = None


class JugadorOportunidad(BaseModel):
    """Estructura de salida para jugadores infravalorados."""

    nombre: str
    posicion_principal: PosicionPrincipal
    edad: int
    calificacion_general: int
    valor_real: float
    valor_predicho: float
    oportunidad_eur: float = Field(
        ..., description="Diferencia positiva (predicho - real) en euros"
    )
    oportunidad_pct: float = Field(
        ..., description="Porcentaje de oportunidad respecto al valor real"
    )
    # Formato legible para humanos (ej.: "€49.36M")
    valor_estimado_formateado: Optional[str] = Field(
        None, description="Valor estimado formateado (ej.: '€49.36M')"
    )
    # Eco opcional del nombre si fue provisto en la solicitud
    nombre_corto: Optional[str] = Field(
        None, description="Nombre corto del jugador (eco)"
    )
    nombre_completo: Optional[str] = Field(
        None, description="Nombre completo del jugador (eco)"
    )
    # Campos formateados adicionales solicitados para el endpoint
    valor_real_formateado: Optional[str] = Field(
        None, description="Valor real formateado (ej.: '€53,622,008')"
    )
    valor_predicho_formateado: Optional[str] = Field(
        None, description="Valor predicho formateado (ej.: '€79,065,839')"
    )
    oportunidad_eur_formateado: Optional[str] = Field(
        None, description="Oportunidad formateada en euros"
    )
    oportunidad_pct_formateado: Optional[str] = Field(
        None, description="Porcentaje de oportunidad formateado (ej.: '17.2%')"
    )


class JugadorEntradaValoracion(JugadorEntrada):
    """
    Extiende la entrada básica con campos opcionales para valoración comparativa.
    """

    valor_real: Optional[float] = Field(
        None, description="Valor actual de mercado en euros para comparar"
    )
    tolerancia_relativa: float = Field(
        0.05,
        ge=0.0,
        le=1.0,
        description="Umbral relativo para considerar 'similar' (ej.: 0.05 = 5%)",
    )


class ValoracionRespuesta(BaseModel):
    """
    Respuesta que incluye la predicción y la clasificación de valoración.
    """

    id_jugador: Optional[str] = None
    valor_predicho: float = Field(..., description="Valor estimado por el modelo (EUR)")
    valor_real: Optional[float] = Field(
        None, description="Valor actual de mercado (EUR), si fue proporcionado"
    )
    clasificacion: Optional[str] = Field(
        None,
        description=(
            "INFRAVALORADO | SOBREVALORADO | BIEN VALORADO | SIN_COMPARACION"
        ),
    )
    diferencia: Optional[float] = Field(
        None, description="valor_predicho - valor_real (EUR)"
    )
    diferencia_relativa: Optional[float] = Field(
        None, description="|diferencia| / max(|valor_predicho|, 1e-9)"
    )
    moneda: str = Field("EUR", description="Moneda usada en la respuesta")
    # Formatos legibles
    valor_predicho_formateado: Optional[str] = Field(
        None, description="Valor predicho formateado (ej.: '€49.36M')"
    )
    valor_real_formateado: Optional[str] = Field(
        None, description="Valor real formateado (ej.: '€60.00M')"
    )
    diferencia_formateada: Optional[str] = Field(
        None, description="Diferencia formateada (ej.: '+€1.25M' o '€-0.75M')"
    )
    # Eco opcional del nombre si fue provisto en la solicitud
    nombre_corto: Optional[str] = Field(
        None, description="Nombre corto del jugador (eco)"
    )
    nombre_completo: Optional[str] = Field(
        None, description="Nombre completo del jugador (eco)"
    )


class ComparacionEntrada(BaseModel):
    """
    Entrada para comparar 2–5 jugadores rápidamente.
    """

    jugadores: List[JugadorEntradaValoracion] = Field(
        ..., min_items=2, max_items=5, description="Lista de jugadores a comparar (2–5)"
    )
    orden: str = Field(
        "gap_desc",
        description=(
            "Criterio de ranking: 'gap_desc' (diferencia desc), 'pred_desc' (valor_predicho desc)"
        ),
    )


class ComparacionItem(BaseModel):
    """Item con resultados de predicción y valoración para un jugador."""

    id_jugador: Optional[str] = None
    nombre_corto: Optional[str] = None
    nombre_completo: Optional[str] = None
    valor_predicho: float
    valor_real: Optional[float] = None
    clasificacion: Optional[str] = None
    diferencia: Optional[float] = None
    diferencia_relativa: Optional[float] = None
    moneda: str = Field("EUR", description="Moneda usada en la respuesta")
    # Formatos legibles
    valor_predicho_formateado: Optional[str] = None
    valor_real_formateado: Optional[str] = None
    diferencia_formateada: Optional[str] = None


class ComparacionRespuesta(BaseModel):
    """Respuesta de comparación con ranking y detalle por jugador."""

    total: int
    orden: str
    items: List[ComparacionItem]
    ranking: List[ComparacionItem]


class EvaluacionSimpleEntrada(BaseModel):
    """
    Entrada simplificada para obtener un resumen rápido usando solo:
    - posicion_principal
    - edad
    - calificacion_general
    - valor_real (para calcular sobreprecio/oportunidad)
    """

    posicion_principal: PosicionPrincipal
    edad: int = Field(..., ge=14, le=50)
    calificacion_general: int = Field(..., ge=1, le=99)
    valor_real: float = Field(..., ge=0)
    pie_preferido: PiePreferido = PiePreferido.Right


class EvaluacionSimpleRespuesta(BaseModel):
    """Respuesta compacta enfocada en los campos solicitados."""

    posicion_principal: PosicionPrincipal
    edad: int
    calificacion_general: int
    valor_real: float
    valor_predicho: float
    etiqueta: str = Field(
        ..., description="OPORTUNIDAD (infravalorado) o SOBREPRECIO (sobrevalorado)"
    )
    diferencia_eur: float = Field(..., description="|real - predicho| en euros")
    porcentaje: float = Field(
        ..., description="diferencia_eur / valor_real * 100"
    )
    # Formatos en euros
    valor_real_formateado: Optional[str] = None
    valor_predicho_formateado: Optional[str] = None
    diferencia_formateada: Optional[str] = None
    porcentaje_formateado: Optional[str] = None


class JugadorSobreprecio(BaseModel):
    """Estructura de salida para jugadores sobrevalorados (sobreprecio)."""

    nombre: str
    posicion_principal: PosicionPrincipal
    edad: int
    calificacion_general: int
    valor_real: float
    valor_predicho: float
    sobreprecio_eur: float = Field(
        ..., description="Diferencia positiva (real - predicho) en euros"
    )
    sobreprecio_pct: float = Field(
        ..., description="Porcentaje de sobreprecio respecto al valor real"
    )
    # Campos formateados
    valor_real_formateado: Optional[str] = None
    valor_predicho_formateado: Optional[str] = None
    sobreprecio_eur_formateado: Optional[str] = None
    sobreprecio_pct_formateado: Optional[str] = None
