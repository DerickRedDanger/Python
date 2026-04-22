LOG_RECORD_SCHEMA = {
    # --------------------------------------------------------
    # Identity & Structure
    # --------------------------------------------------------

    "call_id": int,
    # Unique, monotonically increasing identifier for this call.
    # Assigned at function entry. Chronological across the entire run.

    "root_call_id": int,
    # call_id of the root (progenitor) of this call tree.
    # Equals call_id if this call has no parent.

    "parent_call_id": int | None,
    # call_id of the direct caller, or None if this is a root call.

    "depth": int,
    # Call stack depth at the moment of invocation.
    # Root calls start at depth = 0.

    # --------------------------------------------------------
    # Function Identity
    # --------------------------------------------------------

    "function_name": str,
    # func.__name__
    # Short function name (not guaranteed to be unique).

    "qualified_name": str,
    # func.__qualname__
    # Fully qualified name including class / nesting context.

    "location": {
        # Where the function is defined
        "definition": {
            "module": str,   # func.__module__
            "file": str,     # func.__code__.co_filename
            "line": int,     # func.__code__.co_firstlineno
        },
    
        # Where this specific call was made from
        "callsite": {
            "module": str,   # caller frame __name__
            "file": str,     # caller frame filename
            "line": int,     # caller frame line number
        }
    }

    # --------------------------------------------------------
    # Call Context
    # --------------------------------------------------------

    "call_number": int,
    # Per-function invocation counter.
    # Increments each time this function is called.

    "tag": str | None,
    # Optional user-defined tag for grouping or semantic labeling.

    "parent_tag": str | None,
    # Tag of the direct parent call, if any.

    # --------------------------------------------------------
    # Timing
    # --------------------------------------------------------

    "timestamp_start": str,
    # Human-readable timestamp when the function was entered.
    # Format: YYYY-MM-DD HH:MM:SS.mmm

    "timestamp_end": str,
    # Human-readable timestamp when the function exited.

    "duration": float,
    # Execution duration in seconds (end - start).

    # --------------------------------------------------------
    # Execution Outcome
    # --------------------------------------------------------

    "status": str,
    # Execution status enum:
    # - "ok"        : no warnings, no exceptions
    # - "warning"   : completed, but warnings were raised
    # - "exception" : function raised an exception

    "error": str | None,
    # Full traceback string if an exception occurred, else None.

    # --------------------------------------------------------
    # Arguments / Return — Materialized (Human-readable)
    # --------------------------------------------------------

    "args_repr": str,
    # Materialized string representation of positional arguments.
    # Truncated according to materialization rules.

    "kwargs_repr": str,
    # Materialized string representation of keyword arguments.

    "result_repr": str | None,
    # Materialized string representation of the return value.
    # None if function raised before returning.

    # --------------------------------------------------------
    # Arguments / Return — Metadata (Structured)
    # --------------------------------------------------------

    "args_meta": dict,
    # Structured metadata about positional arguments.
    # Example: {"count": 2, "types": ["int", "list"], "sizes": [None, 1000]}

    "kwargs_meta": dict,
    # Structured metadata about keyword arguments.

    "result_meta": dict | None,
    # Structured metadata about the return value.
    # Example: {"type": "ndarray", "shape": (100, 3)}

    # --------------------------------------------------------
    # Warnings
    # --------------------------------------------------------

    "warnings_meta": list[dict] | None,
    # List of captured warnings, each with:
    # {"type", "message", "file", "line"}

}
