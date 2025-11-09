import os
import time
import uuid
from collections import deque
from typing import Callable, Deque, Dict, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware que asegura un ID de correlación por solicitud.
    - Lee `X-Request-ID` si viene del cliente; caso contrario genera un UUID4.
    - Expone el ID en `request.state.request_id` y lo devuelve en la respuesta.
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Limitador de tasa en memoria (por IP) con ventana deslizante de 60 s.

    Configuración por variables de entorno:
      - RATE_LIMIT_PER_MIN: solicitudes por minuto (default: 60)
      - RATE_LIMIT_WINDOW_SEC: segundos de ventana (default: 60)
    """

    def __init__(self, app):
        super().__init__(app)
        self.limite = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))
        self.ventana = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))
        self._hits: Dict[str, Deque[float]] = {}

    def _clave_cliente(self, request: Request) -> str:
        # Respeta proxies si están configurados
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next: Callable):
        clave = self._clave_cliente(request)
        ahora = time.time()
        inicio_ventana = ahora - self.ventana

        q = self._hits.get(clave)
        if q is None:
            q = deque()
            self._hits[clave] = q

        # limpiar eventos fuera de la ventana
        while q and q[0] < inicio_ventana:
            q.popleft()

        if len(q) >= self.limite:
            # 429 Too Many Requests
            return Response(
                status_code=429,
                content="{\"detail\": \"Rate limit excedido\"}",
                media_type="application/json",
                headers={"Retry-After": str(self.ventana)},
            )

        q.append(ahora)
        return await call_next(request)

