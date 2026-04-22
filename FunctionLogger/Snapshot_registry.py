SNAPSHOT_REGISTRY: dict[int, SnapshotBundle]

SnapshotBundle = {
    "run_id": int,  # must match Run Table primary key

    "origin": Literal["normal", "error"],
    # Final highest-severity state of the call.
    # Priority: error > warning > normal

    "strategy": Literal["ref", "copy", "deepcopy"],
    # Strategy actually used to capture snapshot.

    "args": Any | None,
    "kwargs": dict | None,
    "result": Any | None,
    # Snapshot payload. None if not captured.

    "has_result": bool,
    # True if function produced a return value,
    # including error_return cases.

    "note": str | None,
    # Optional short explanation (e.g., "exception",
    # "timeout_error", "error_return").
}