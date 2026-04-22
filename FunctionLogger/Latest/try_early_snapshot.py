import copy
from typing import Literal


def try_early_snapshot(
    *,
    value: Any,
    name: str,
    normal_strategy: SnapshotStrategy,
    error_strategy: SnapshotStrategy,
    size_limit_bytes: Optional[int],
) -> tuple[Any, list[SnapshotNote], set[Literal["normal", "error"]]]:
    """
    Capture an early snapshot only when normal and/or error strategy
    requires deepcopy fidelity before mutation.

    Returns:
        (snapshot_value, notes, origins)

    Where:
        snapshot_value:
            - deepcopy(value) if successful
            - original value if degraded to ref
            - None if no early snapshot was needed

        notes:
            Structured notes explaining degradation, if any.

        origins:
            Which final origins this early snapshot applies to:
            - {"normal"}
            - {"error"}
            - {"normal", "error"}
            - empty set if no early snapshot was needed
    """
    notes: list[SnapshotNote] = []
    origins: set[Literal["normal", "error"]] = set()

    # ---------------------------------
    # 1. Determine whether early snapshot is needed
    # ---------------------------------
    if normal_strategy == "deepcopy":
        origins.add("normal")

    if error_strategy == "deepcopy":
        origins.add("error")

    if not origins:
        return None, notes, origins

    # ---------------------------------
    # 2. Estimate size BEFORE deepcopy
    # ---------------------------------
    estimated_size = estimate_size_bytes(value)

    if (
        size_limit_bytes is not None
        and estimated_size is not None
        and estimated_size > size_limit_bytes
    ):
        notes.append((
            f"{name}_snapshot",
            "degraded_due_to_size_limit",
            f"estimated_size={estimated_size}, limit={size_limit_bytes}",
        ))
        return value, notes, origins  # degrade to ref

    # ---------------------------------
    # 3. Try deepcopy
    # ---------------------------------
    try:
        snap = copy.deepcopy(value)
        return snap, notes, origins

    except Exception as exc:
        notes.append((
            f"{name}_snapshot",
            "deepcopy_failed_degraded_to_ref",
            str(exc),
        ))
        return value, notes, origins  # degrade to ref