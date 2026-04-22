RUN_RECORD_SCHEMA = {
    # --------------------------------------------------------
    # Identity & Structure
    # --------------------------------------------------------

    "run_id": int,
    # Unique, monotonically increasing identifier for this function execution.
    # Assigned at function entry. Chronological across the entire program run.

    "root_run_id": int,
    # run_id of the root (progenitor) of this call tree.
    # Equals run_id if this call has no parent.

    "parent_run_id": int | None,
    # run_id of the direct caller, or None if this is a root call.

    "depth": int,
    # Call stack depth at invocation time. Root calls start at 0.

    # --------------------------------------------------------
    # Function Identity
    # --------------------------------------------------------

    "function_name": str,
    # func.__name__
    # Short, human-readable function name (not guaranteed unique).

    "qualified_name": str,
    # func.__qualname__
    # Fully qualified name including class / nesting context.

    "module_name": str,
    # func.__module__
    # Module where the function is defined.

    "defined_file": str,
    # Source file path where the function is defined.

    "defined_line": int,
    # Line number of the function definition.

    # --------------------------------------------------------
    # Call Context
    # --------------------------------------------------------

    "tag": str | None,
    # Optional user-defined semantic tag.

    "called_file": str,
    # Source file where this function call occurred.

    "called_line": int,
    # Line number where this function was called.

    "call_number": int,
    # Per-function invocation counter.
    # Helps compare multiple executions of the same function.

    # --------------------------------------------------------
    # Timing
    # --------------------------------------------------------

    "timestamp_start": float,
    # Monotonic or epoch timestamp when function execution started.

    "timestamp_end": float,
    # Timestamp when function execution finished.

    "duration": float,
    # Execution duration in seconds.

    # --------------------------------------------------------
    # Execution Outcome (Derived / Summary)
    # --------------------------------------------------------

    "status": str,
    # Enum:
    # - "ok"
    # - "warning"
    # - "error"

    "n_events": int,
    # Total number of events (warnings + errors) emitted by this run.

    "error_return_used": bool,
    # True if an exception occurred but a return value was supplied.

    "error_return_repr": str | None,
    # Representation of the value returned after error interception.

    # --------------------------------------------------------
    # Arguments / Return — Representation
    # --------------------------------------------------------

    "args_repr": str,
    # Materialized, truncated string representation of positional arguments.

    "kwargs_repr": str,
    # Materialized, truncated string representation of keyword arguments.

    "result_repr": str | None,
    # Materialized representation of the return value.
    # None if the function did not return normally.

    # --------------------------------------------------------
    # Arguments / Return — Metadata
    # --------------------------------------------------------

    "args_meta": dict,
    # Structured metadata about positional arguments.

    "kwargs_meta": dict,
    # Structured metadata about keyword arguments.

    "result_meta": dict | None,
    # Structured metadata about the return value.
}


