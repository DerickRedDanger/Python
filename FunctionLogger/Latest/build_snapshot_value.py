import copy
from typing import Any, Optional


def build_snapshot_value(
    *,
    field_name: str,
    strategy: SnapshotStrategy,
    value: Any,
    size_limit_bytes: Optional[int],
    has_value: bool = True,
) -> SnapshotValue:
    """
    Build a SnapshotValue for one field (args / kwargs / result).

    Parameters:
        field_name:
            Logical field name, usually "args", "kwargs", or "result".

        strategy:
            One of:
            - None / "none"
            - "ref"
            - "copy"
            - "deepcopy"

        value:
            The current value to snapshot.

        size_limit_bytes:
            Optional size limit used only for deepcopy.

        has_value:
            Whether a value truly exists to snapshot.
            Mainly relevant for `result`, where a function may have raised
            and re-raised before producing any result.

    Returns:
        SnapshotValue
    """

    # ---------------------------------
    # 1. Snapshot disabled by policy
    # ---------------------------------
    if strategy is None or strategy == "none":
        return SnapshotValue(
            captured=False,
            strategy="none",
            value=None,
            notes=[(
                f"{field_name}_snapshot",
                "disabled_by_policy",
                "snapshot disabled",
            )],
        )

    # ---------------------------------
    # 2. No value exists to snapshot
    # ---------------------------------
    if not has_value:
        reason = (
            "no_result_due_to_exception"
            if field_name == "result"
            else "no_value"
        )
        description = (
            "function raised before producing a result"
            if field_name == "result"
            else "nothing to snapshot"
        )

        return SnapshotValue(
            captured=False,
            strategy=None,
            value=None,
            notes=[(
                f"{field_name}_snapshot",
                reason,
                description,
            )],
        )

    # ---------------------------------
    # 3. Reference strategy
    # ---------------------------------
    if strategy == "ref":
        return SnapshotValue(
            captured=True,
            strategy="ref",
            value=value,
            notes=[],
        )

    # ---------------------------------
    # 4. Shallow copy strategy
    # ---------------------------------
    if strategy == "copy":
        try:
            copied = copy.copy(value)
            return SnapshotValue(
                captured=True,
                strategy="copy",
                value=copied,
                notes=[],
            )
        except Exception as exc:
            return SnapshotValue(
                captured=True,
                strategy="ref",
                value=value,
                notes=[(
                    f"{field_name}_snapshot",
                    "copy_failed_degraded_to_ref",
                    str(exc),
                )],
            )

    # ---------------------------------
    # 5. Deep copy strategy
    # ---------------------------------
    if strategy == "deepcopy":
        estimated_size = estimate_size_bytes(value)

        if (
            size_limit_bytes is not None
            and estimated_size is not None
            and estimated_size > size_limit_bytes
        ):
            return SnapshotValue(
                captured=True,
                strategy="ref",
                value=value,
                notes=[(
                    f"{field_name}_snapshot",
                    "degraded_due_to_size_limit",
                    f"estimated_size={estimated_size}, limit={size_limit_bytes}",
                )],
            )

        try:
            copied = copy.deepcopy(value)
            return SnapshotValue(
                captured=True,
                strategy="deepcopy",
                value=copied,
                notes=[],
            )
        except Exception as exc:
            return SnapshotValue(
                captured=True,
                strategy="ref",
                value=value,
                notes=[(
                    f"{field_name}_snapshot",
                    "deepcopy_failed_degraded_to_ref",
                    str(exc),
                )],
            )

    # ---------------------------------
    # 6. Defensive fallback
    # ---------------------------------
    return SnapshotValue(
        captured=False,
        strategy=None,
        value=None,
        notes=[(
            f"{field_name}_snapshot",
            "unknown_strategy",
            f"strategy={strategy!r}",
        )],
    )