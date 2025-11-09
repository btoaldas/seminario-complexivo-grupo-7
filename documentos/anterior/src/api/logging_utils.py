import json
import logging
import time
from typing import Any, Dict


def configurar_logging() -> None:
    """Configura logging simple en formato JSON a stdout."""
    if getattr(configurar_logging, "_configurado", False):
        return

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            payload = {
                "level": record.levelname,
                "msg": record.getMessage(),
                "logger": record.name,
                "time": int(time.time() * 1000),
            }
            # Campos extra si existen
            if hasattr(record, "extra") and isinstance(record.extra, dict):
                payload.update(record.extra)  # type: ignore[arg-type]
            return json.dumps(payload, ensure_ascii=False)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)

    configurar_logging._configurado = True  # type: ignore[attr-defined]


def log_event(evento: str, **extra: Any) -> None:
    """
    Registra un evento con metadatos en JSON.

    Args:
        evento: Nombre del evento.
        extra: Pares clave/valor adicionales.
    """
    logger = logging.getLogger("scouting_fifa")
    # Empaquetar como un solo dict para el formateador
    record = logging.LogRecord(
        name=logger.name,
        level=logging.INFO,
        pathname=__file__,
        lineno=0,
        msg=evento,
        args=(),
        exc_info=None,
    )
    record.extra = extra  # type: ignore[attr-defined]
    for h in logging.getLogger().handlers:
        h.handle(record)

