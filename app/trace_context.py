from contextvars import ContextVar

current_session_id = ContextVar(
    "current_session_id",
    default=None
)

current_turn_id = ContextVar(
    "current_turn_id",
    default=None
)

