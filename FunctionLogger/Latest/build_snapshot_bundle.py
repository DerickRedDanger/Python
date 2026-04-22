def build_snapshot_bundle(
    *,
    state: CallState,
    config: ResolvedConfig,
    args,
    kwargs,
) -> SnapshotBundle:
    """
    Build the final runtime-only snapshot bundle for this call.

    Rules:
    - origin is only "normal" or "error"
    - warnings and timeout do not change snapshot origin
    - early snapshots are used only if their stored origins include
      the final origin of this call
    """

    # ---------------------------------
    # 1. Final snapshot origin
    # ---------------------------------
    origin: SnapshotOrigin = "error" if state.raised_exception else "normal"

    # ---------------------------------
    # 2. Resolve strategies for this origin
    # ---------------------------------
    if origin == "error":
        arg_strategy = config.error_arg_snapshot
        kwargs_strategy = config.error_kwargs_snapshot
        result_strategy = config.error_result_snapshot
    else:
        arg_strategy = config.arg_snapshot
        kwargs_strategy = config.kwargs_snapshot
        result_strategy = config.result_snapshot

    # ---------------------------------
    # 3. Args snapshot
    # Use early snapshot only if it was captured
    # for this exact origin
    # ---------------------------------
    if origin in state.early_args_origins:
        # strategy reflects what actually happened early:
        # deepcopy if clean, ref if degraded
        early_args_strategy = (
            "ref" if state.early_args_notes else "deepcopy"
        )

        args_snapshot = SnapshotValue(
            captured=True,
            strategy=early_args_strategy,
            value=state.early_args_snapshot,
            notes=list(state.early_args_notes),
        )
    else:
        args_snapshot = build_snapshot_value(
            field_name="args",
            strategy=arg_strategy,
            value=args,
            size_limit_bytes=config.snapshot_size_limit_bytes,
            has_value=True,
        )

    # ---------------------------------
    # 4. Kwargs snapshot
    # ---------------------------------
    if origin in state.early_kwargs_origins:
        early_kwargs_strategy = (
            "ref" if state.early_kwargs_notes else "deepcopy"
        )

        kwargs_snapshot = SnapshotValue(
            captured=True,
            strategy=early_kwargs_strategy,
            value=state.early_kwargs_snapshot,
            notes=list(state.early_kwargs_notes),
        )
    else:
        kwargs_snapshot = build_snapshot_value(
            field_name="kwargs",
            strategy=kwargs_strategy,
            value=kwargs,
            size_limit_bytes=config.snapshot_size_limit_bytes,
            has_value=True,
        )

    # ---------------------------------
    # 5. Result snapshot
    # There is never an early result snapshot
    # ---------------------------------
    result_snapshot = build_snapshot_value(
        field_name="result",
        strategy=result_strategy,
        value=state.result if state.has_result else None,
        size_limit_bytes=config.snapshot_size_limit_bytes,
        has_value=state.has_result,
    )

    # ---------------------------------
    # 6. Build final bundle
    # ---------------------------------
    return SnapshotBundle(
        call_id=state.call_id,
        origin=origin,
        args=args_snapshot,
        kwargs=kwargs_snapshot,
        result=result_snapshot,
        result_exists=state.has_result,
    )