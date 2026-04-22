from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Literal


# ============================================================
# Sentinels
# ============================================================

_USE_PROFILE = object()
_USE_LOGGER_PROFILE = object()
RE_RAISE = object()
_UNSET = object()


# ============================================================
# Type aliases
# ============================================================

SnapshotStrategy = Optional[Literal["none", "ref", "copy", "deepcopy"]]
_ALLOWED_SNAPSHOT_STRATEGIES = {None, "none", "ref", "copy", "deepcopy"}


# ============================================================
# Profile objects
# ============================================================

@dataclass(frozen=True, slots=True)
class LoggerProfile:
    default_snapshot_strategy: SnapshotStrategy
    snapshot_size_limit_mb: Optional[float]

    arg_snapshot: SnapshotStrategy
    kwargs_snapshot: SnapshotStrategy
    result_snapshot: SnapshotStrategy

    error_arg_snapshot: SnapshotStrategy
    error_kwargs_snapshot: SnapshotStrategy
    error_result_snapshot: SnapshotStrategy

    timeout: Optional[float]
    error_return: Any


@dataclass(frozen=True, slots=True)
class DecoratorProfile:
    default_snapshot_strategy: SnapshotStrategy
    snapshot_size_limit_mb: Optional[float]

    arg_snapshot: SnapshotStrategy
    kwargs_snapshot: SnapshotStrategy
    result_snapshot: SnapshotStrategy

    error_arg_snapshot: SnapshotStrategy
    error_kwargs_snapshot: SnapshotStrategy
    error_result_snapshot: SnapshotStrategy

    timeout: Optional[float]
    error_return: Any

    tag: Optional[str]


# ============================================================
# Defaults
# ============================================================

_LOGGER_PROFILE_DEFAULTS = {
    "default_snapshot_strategy": "ref",
    "snapshot_size_limit_mb": 10,

    "arg_snapshot": None,
    "kwargs_snapshot": None,
    "result_snapshot": None,

    "error_arg_snapshot": "deepcopy",
    "error_kwargs_snapshot": "deepcopy",
    "error_result_snapshot": "deepcopy",

    "timeout": None,
    "error_return": RE_RAISE,
}

_DECORATOR_PROFILE_DEFAULTS = {
    **_LOGGER_PROFILE_DEFAULTS,
    "tag": None,
}


# ============================================================
# Helpers
# ============================================================

def _validate_snapshot_strategy(value: Any, field_name: str) -> None:
    if value not in _ALLOWED_SNAPSHOT_STRATEGIES:
        raise ValueError(
            f"Invalid value for {field_name}: {value!r}. "
            f"Expected one of: None, 'none', 'ref', 'copy', 'deepcopy'."
        )


def _validate_timeout(value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, (int, float)) or value < 0:
        raise ValueError("timeout must be None or a non-negative number")


def _validate_snapshot_size_limit_mb(value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError("snapshot_size_limit_mb must be None or a positive number")


def _validate_tag(value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        raise ValueError("tag must be None or a string")


def _validate_config_keys(config: Mapping[str, Any], allowed_keys: set[str], profile_name: str) -> None:
    unknown = set(config.keys()) - allowed_keys
    if unknown:
        allowed_str = ", ".join(sorted(allowed_keys))
        unknown_str = ", ".join(sorted(unknown))
        raise ValueError(
            f"Unknown keys for {profile_name}: {unknown_str}. "
            f"Allowed keys are: {allowed_str}"
        )


def _resolve_factory_field(
    *,
    field_name: str,
    config: Mapping[str, Any],
    base_value: Any,
    default_value: Any,
) -> Any:
    if field_name in config:
        return config[field_name]
    if base_value is not _UNSET:
        return base_value
    return default_value


def _base_logger_value(base: LoggerProfile | None, field_name: str) -> Any:
    if base is None:
        return _UNSET
    return getattr(base, field_name)


def _base_decorator_value(base: DecoratorProfile | LoggerProfile | None, field_name: str) -> Any:
    if base is None:
        return _UNSET
    return getattr(base, field_name, _UNSET)


# ============================================================
# Factories
# ============================================================

def build_logger_profile(
    *,
    base: LoggerProfile | None = None,
    config: Mapping[str, Any] | None = None,
) -> LoggerProfile:
    """
    Build and validate a LoggerProfile.

    Precedence:
        config[field] -> base.field -> hard default
    """
    config = dict(config or {})

    allowed_keys = {
        "default_snapshot_strategy",
        "snapshot_size_limit_mb",

        "arg_snapshot",
        "kwargs_snapshot",
        "result_snapshot",

        "error_arg_snapshot",
        "error_kwargs_snapshot",
        "error_result_snapshot",

        "timeout",
        "error_return",
    }
    _validate_config_keys(config, allowed_keys, "LoggerProfile")

    resolved = {
        field: _resolve_factory_field(
            field_name=field,
            config=config,
            base_value=_base_logger_value(base, field),
            default_value=_LOGGER_PROFILE_DEFAULTS[field],
        )
        for field in allowed_keys
    }

    # Validation
    _validate_snapshot_strategy(resolved["default_snapshot_strategy"], "default_snapshot_strategy")
    _validate_snapshot_size_limit_mb(resolved["snapshot_size_limit_mb"])

    for field in ("arg_snapshot", "kwargs_snapshot", "result_snapshot"):
        _validate_snapshot_strategy(resolved[field], field)

    for field in ("error_arg_snapshot", "error_kwargs_snapshot", "error_result_snapshot"):
        _validate_snapshot_strategy(resolved[field], field)

    _validate_timeout(resolved["timeout"])
    # error_return intentionally left flexible

    return LoggerProfile(**resolved)


def build_decorator_profile(
    *,
    base: DecoratorProfile | LoggerProfile | None = None,
    config: Mapping[str, Any] | None = None,
    tag: str | None | object = _UNSET,
) -> DecoratorProfile:
    """
    Build and validate a DecoratorProfile.

    Precedence:
        tag kwarg -> config['tag'] -> base.tag -> hard default
        all other fields:
            config[field] -> base.field -> hard default
    """
    config = dict(config or {})

    allowed_keys = {
        "default_snapshot_strategy",
        "snapshot_size_limit_mb",

        "arg_snapshot",
        "kwargs_snapshot",
        "result_snapshot",

        "error_arg_snapshot",
        "error_kwargs_snapshot",
        "error_result_snapshot",

        "timeout",
        "error_return",

        "tag",
    }
    _validate_config_keys(config, allowed_keys, "DecoratorProfile")

    resolved = {
        field: _resolve_factory_field(
            field_name=field,
            config=config,
            base_value=_base_decorator_value(base, field),
            default_value=_DECORATOR_PROFILE_DEFAULTS[field],
        )
        for field in allowed_keys
        if field != "tag"
    }

    # tag has special override precedence
    if tag is not _UNSET:
        resolved_tag = tag
    elif "tag" in config:
        resolved_tag = config["tag"]
    else:
        base_tag = _base_decorator_value(base, "tag")
        resolved_tag = None if base_tag is _UNSET else base_tag
        if resolved_tag is None:
            resolved_tag = _DECORATOR_PROFILE_DEFAULTS["tag"]

    resolved["tag"] = resolved_tag

    # Validation
    _validate_snapshot_strategy(resolved["default_snapshot_strategy"], "default_snapshot_strategy")
    _validate_snapshot_size_limit_mb(resolved["snapshot_size_limit_mb"])

    for field in ("arg_snapshot", "kwargs_snapshot", "result_snapshot"):
        _validate_snapshot_strategy(resolved[field], field)

    for field in ("error_arg_snapshot", "error_kwargs_snapshot", "error_result_snapshot"):
        _validate_snapshot_strategy(resolved[field], field)

    _validate_timeout(resolved["timeout"])
    _validate_tag(resolved["tag"])
    # error_return intentionally left flexible

    return DecoratorProfile(**resolved)


# ============================================================
# Built-in profiles
# ============================================================

class LP:
    LIGHTWEIGHT = build_logger_profile()

    DEBUG = build_logger_profile(
        config={
            "default_snapshot_strategy": "deepcopy",
            "snapshot_size_limit_mb": 50,
        }
    )

    MINIMAL = build_logger_profile(
        config={
            "default_snapshot_strategy": "none",
            "error_arg_snapshot": "ref",
            "error_kwargs_snapshot": "ref",
            "error_result_snapshot": "ref",
        }
    )


class DP:
    DEFAULT = build_decorator_profile()

    LIGHTWEIGHT = build_decorator_profile(
        config={
            "default_snapshot_strategy": "ref",
            "snapshot_size_limit_mb": 10,
        }
    )

    NO_SNAPSHOT = build_decorator_profile(
        config={
            "default_snapshot_strategy": "none",
        }
    )

    STRICT = build_decorator_profile(
        config={
            "default_snapshot_strategy": "deepcopy",
            "snapshot_size_limit_mb": 50,
        }
    )