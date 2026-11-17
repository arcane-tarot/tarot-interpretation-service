from prometheus_client import Counter, Histogram


HTTP_REQUESTS = Counter(
    "tarot_http_requests_total",
    "Total HTTP requests received by the backend",
    ["method", "route", "status_code"],
)

HTTP_REQUEST_DURATION = Histogram(
    "tarot_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route"],
)

OPENAI_REQUESTS = Counter(
    "tarot_openai_requests_total",
    "Requests made to the configured OpenAI-compatible service",
    ["outcome"],
)

OPENAI_REQUEST_DURATION = Histogram(
    "tarot_openai_request_duration_seconds",
    "Duration of calls to the OpenAI-compatible service",
)