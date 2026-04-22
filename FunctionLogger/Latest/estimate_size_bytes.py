import sys
from typing import Any, Optional


def estimate_size_bytes(value: Any) -> Optional[int]:
    """
    Best-effort size estimate in bytes.

    Returns:
        int: estimated size in bytes
        None: if size could not be estimated safely
    """
    try:
        return sys.getsizeof(value)
    except Exception:
        return None