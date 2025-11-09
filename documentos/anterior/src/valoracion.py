"""
Utilidades para clasificar valoración de un jugador dado el valor predicho
y (opcional) el valor real.

Reglas:
- Si no hay `valor_real`: clasificacion = "SIN_COMPARACION".
- Si |gap| <= tolerancia_relativa * max(valor_predicho, 1): "BIEN VALORADO".
- Si gap > 0: "INFRAVALORADO" (predicho > real).
- Si gap < 0: "SOBREVALORADO".
"""

from typing import Dict, Optional


def evaluar_valoracion(
    valor_predicho: float,
    valor_real: Optional[float] = None,
    tolerancia_relativa: float = 0.05,
) -> Dict[str, Optional[float | str]]:
    """Evalúa la valoración relativa de un jugador.

    Args:
        valor_predicho: Salida del modelo (EUR).
        valor_real: Valor actual de mercado (EUR). Si es None, no hay comparación.
        tolerancia_relativa: Umbral relativo para considerar que los valores son similares.

    Returns:
        Diccionario con `valor_predicho`, `valor_real`, `clasificacion`,
        `diferencia` y `diferencia_relativa`.
    """

    res: Dict[str, Optional[float | str]] = {
        "valor_predicho": float(valor_predicho),
        "valor_real": float(valor_real) if valor_real is not None else None,
        "clasificacion": None,
        "diferencia": None,
        "diferencia_relativa": None,
    }

    if valor_real is None:
        res["clasificacion"] = "SIN_COMPARACION"
        return res

    gap = float(valor_predicho) - float(valor_real)
    denom = max(abs(float(valor_predicho)), 1.0)
    rel = abs(gap) / denom
    res["diferencia"] = gap
    res["diferencia_relativa"] = rel

    if rel <= tolerancia_relativa:
        res["clasificacion"] = "BIEN VALORADO"
    elif gap > 0:
        res["clasificacion"] = "INFRAVALORADO"
    else:
        res["clasificacion"] = "SOBREVALORADO"

    return res

