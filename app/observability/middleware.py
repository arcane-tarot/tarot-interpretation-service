import time

from fastapi import Request

from app.observability.metrics import (
    HTTP_REQUEST_DURATION,
    HTTP_REQUESTS,
)

EXCLUDED_PATHS = {
    "/metrics",
    "/health",
    "/health/live",
    "/health/ready",
    "/health/startup",
}


async def metrics_middleware(request: Request, call_next):
    if request.url.path in EXCLUDED_PATHS:
        return await call_next(request)

    started_at = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        route_path = getattr(route, "path", "unmatched")

        HTTP_REQUESTS.labels(
            method=request.method,
            route=route_path,
            status_code=str(status_code),
        ).inc()

        HTTP_REQUEST_DURATION.labels(
            method=request.method,
            route=route_path,
        ).observe(time.perf_counter() - started_at)
