EVENT_RECORD_SCHEMA = {
    # --------------------------------------------------------
    # Identity
    # --------------------------------------------------------

    "event_id": int,
    # Unique, monotonically increasing identifier for this event.

    "run_id": int,
    # run_id of the function execution that emitted this event.

    # --------------------------------------------------------
    # Event Classification
    # --------------------------------------------------------

    "event_type": str,
    # Enum:
    # - "warning"
    # - "error"

    "category": str,
    # Warning class name or Exception class name.
    # Example: "UserWarning", "ValueError"

    "message": str,
    # Event message string.

    # --------------------------------------------------------
    # Source Location
    # --------------------------------------------------------

    "file": str,
    # Source file where the warning/error originated.

    "line": int,
    # Line number in the source file.

    # --------------------------------------------------------
    # Timing
    # --------------------------------------------------------

    "timestamp": float,
    # Timestamp when the event occurred.

    # --------------------------------------------------------
    # Error-specific (optional)
    # --------------------------------------------------------

    "traceback": str | None,
    # Full traceback string (errors only).
}
