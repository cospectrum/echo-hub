import contextvars


trace_id = contextvars.ContextVar("trace_id", default="N/A")
