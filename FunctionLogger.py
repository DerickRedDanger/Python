def log_function(
    self,
    *,
    profile=_USE_LOGGER_PROFILE,
    tag=_USE_PROFILE,

    default_snapshot_strategy=_USE_PROFILE,
    snapshot_size_limit_mb=_USE_PROFILE,

    arg_snapshot=_USE_PROFILE,
    kwargs_snapshot=_USE_PROFILE,
    result_snapshot=_USE_PROFILE,

    error_arg_snapshot=_USE_PROFILE,
    error_kwargs_snapshot=_USE_PROFILE,
    error_result_snapshot=_USE_PROFILE,

    timeout=_USE_PROFILE,
    error_return=_USE_PROFILE,
):
    def decorator(func):
        if is_generator_function(func):
            raise TypeError(
                "FunctionLogger does not support generator functions."
            )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resolved = resolve_config(
                profile=profile,
                tag=tag,
                default_snapshot_strategy=default_snapshot_strategy,
                snapshot_size_limit_mb=snapshot_size_limit_mb,
                arg_snapshot=arg_snapshot,
                kwargs_snapshot=kwargs_snapshot,
                result_snapshot=result_snapshot,
                error_arg_snapshot=error_arg_snapshot,
                error_kwargs_snapshot=error_kwargs_snapshot,
                error_result_snapshot=error_result_snapshot,
                timeout=timeout,
                error_return=error_return,
                logger_profile=self.profile,
            )

            # ---------------------------------
            # Degraded mode:
            # no logging, no timeout, no snapshots
            # error_return still works
            # ---------------------------------
            if self._degraded:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if resolved.error_return is RE_RAISE:
                        raise
                    return resolved.error_return

            state = None
            phase = "pre_call"
            end_time_wall = None

            try:
                # =================================
                # 1. Build call identity
                # =================================
                call_id = self._next_call_id()

                parent_state = self._stack[-1] if self._stack else None
                root_call_id = parent_state.root_call_id if parent_state else call_id
                parent_call_id = parent_state.call_id if parent_state else None
                depth = len(self._stack)

                function_name = func.__name__
                qualified_name = func.__qualname__
                module_name = func.__module__
                file_name = get_defined_file(func)
                def_line = get_defined_line(func)

                called_file, called_line = get_called_location()
                func_call_index = self._next_func_call_index(qualified_name)

                # =================================
                # 2. Create CallState
                # =================================
                state = CallState(
                    call_id=call_id,
                    root_call_id=root_call_id,
                    parent_call_id=parent_call_id,
                    depth=depth,

                    function_name=function_name,
                    func_call_index=func_call_index,
                    qualified_name=qualified_name,
                    module_name=module_name,
                    file_name=file_name,
                    def_line=def_line,

                    called_file=called_file,
                    called_line=called_line,
                    tag=resolved.tag,

                    start_time_perf=perf_counter(),
                    start_time_wall=time.time(),
                )

                # =================================
                # 3. Capture early repr
                # =================================
                state.args_repr = safe_repr(args)
                state.kwargs_repr = safe_repr(kwargs)

                # =================================
                # 4. Early snapshots
                # only when needed for deepcopy fidelity
                # =================================
                phase = "arg_snapshot"

                if needs_early_args_snapshot(resolved):
                    (
                        state.early_args_snapshot,
                        state.early_args_notes,
                    ) = try_early_snapshot(
                        value=args,
                        name="args",
                        normal_strategy=resolved.arg_snapshot,
                        error_strategy=resolved.error_arg_snapshot,
                        size_limit_bytes=resolved.snapshot_size_limit_bytes,
                    )

                if needs_early_kwargs_snapshot(resolved):
                    (
                        state.early_kwargs_snapshot,
                        state.early_kwargs_notes,
                    ) = try_early_snapshot(
                        value=kwargs,
                        name="kwargs",
                        normal_strategy=resolved.kwargs_snapshot,
                        error_strategy=resolved.error_kwargs_snapshot,
                        size_limit_bytes=resolved.snapshot_size_limit_bytes,
                    )

                # =================================
                # 5. Push stack
                # =================================
                self._stack.append(state)

                # =================================
                # 6. Execute wrapped function
                # =================================
                phase = "execution"

                with warnings.catch_warnings(record=True) as captured_warnings:
                    warnings.simplefilter("always")

                    try:
                        state.result = func(*args, **kwargs)
                        state.has_result = True

                    except Exception as exc:
                        state.raised_exception = True
                        state.exception_object = exc
                        state.traceback_str = traceback.format_exc()

                        if resolved.error_return is not RE_RAISE:
                            state.result = resolved.error_return
                            state.has_result = True
                            state.used_error_return = True

                    finally:
                        state.warnings_captured = list(captured_warnings)

                # =================================
                # 7. Timing + timeout
                # observational only
                # =================================
                state.duration_perf = perf_counter() - state.start_time_perf
                end_time_wall = time.time()

                if resolved.timeout is not None:
                    if state.duration_perf > resolved.timeout:
                        state.timeout_triggered = True

                # =================================
                # 8. Build snapshot bundle
                # =================================
                phase = "result_snapshot"

                snapshot_bundle = build_snapshot_bundle(
                    state=state,
                    config=resolved,
                    args=args,
                    kwargs=kwargs,
                )
                self.snapshot_registry[state.call_id] = snapshot_bundle

                # =================================
                # 9. Write events
                # =================================
                phase = "event_write"
                n_events = 0

                for warn in state.warnings_captured:
                    warn_category = getattr(
                        getattr(warn, "category", None),
                        "__name__",
                        "UnknownWarning",
                    )

                    self._write_event(
                        event_type="warning",
                        category=warn_category,
                        message=str(getattr(warn, "message", "Unknown warning")),
                        details=None,
                        file=getattr(warn, "filename", state.called_file),
                        line=getattr(warn, "lineno", state.called_line),
                        timestamp=end_time_wall,
                        traceback=None,
                        call_id=state.call_id,
                    )
                    n_events += 1

                if state.timeout_triggered:
                    self._write_event(
                        event_type="warning",
                        category="timeout",
                        message="Timeout exceeded",
                        details=f"duration={state.duration_perf}, limit={resolved.timeout}",
                        file=state.called_file,
                        line=state.called_line,
                        timestamp=end_time_wall,
                        traceback=None,
                        call_id=state.call_id,
                    )
                    n_events += 1

                if state.raised_exception:
                    self._write_event(
                        event_type="error",
                        category=type(state.exception_object).__name__,
                        message=str(state.exception_object),
                        details=None,
                        file=state.called_file,
                        line=state.called_line,
                        timestamp=end_time_wall,
                        traceback=state.traceback_str,
                        call_id=state.call_id,
                    )
                    n_events += 1

                # =================================
                # 10. Derive status
                # =================================
                if state.raised_exception:
                    status = "error"
                elif state.warnings_captured or state.timeout_triggered:
                    status = "warning"
                else:
                    status = "ok"

                # =================================
                # 11. Write run row
                # =================================
                phase = "run_write"

                result_repr = safe_repr(state.result) if state.has_result else None

                self._write_run(
                    call_id=state.call_id,
                    root_call_id=state.root_call_id,
                    parent_call_id=state.parent_call_id,
                    depth=state.depth,

                    function_name=state.function_name,
                    qualified_name=state.qualified_name,
                    module_name=state.module_name,
                    defined_file=state.file_name,
                    defined_line=state.def_line,

                    tag=state.tag,
                    called_file=state.called_file,
                    called_line=state.called_line,
                    func_call_index=state.func_call_index,

                    timestamp_start=state.start_time_wall,
                    timestamp_end=end_time_wall,
                    duration=state.duration_perf,

                    status=status,
                    n_events=n_events,

                    error_return_used=state.used_error_return,
                    error_return_repr=result_repr if state.used_error_return else None,

                    args_repr=state.args_repr,
                    kwargs_repr=state.kwargs_repr,
                    result_repr=result_repr,

                    # placeholders
                    args_meta={},
                    kwargs_meta={},
                    result_meta=None,
                )

                # =================================
                # 12. Return / raise
                # =================================
                if state.raised_exception and not state.used_error_return:
                    raise state.exception_object

                return state.result

            except Exception as internal_exc:
                # =================================
                # Internal logger failure
                # =================================
                self._handle_internal_failure(
                    exc=internal_exc,
                    func=func,
                    state=state,
                    args=args,
                    kwargs=kwargs,
                    phase=phase,
                )

                # Safe fallback:
                # only execute func if it has NOT started yet
                if phase in ("pre_call", "arg_snapshot"):
                    try:
                        return func(*args, **kwargs)
                    except Exception:
                        if resolved.error_return is RE_RAISE:
                            raise
                        return resolved.error_return

                # If execution already started, never call func again.
                if state is not None and state.raised_exception:
                    if state.used_error_return:
                        return state.result
                    raise state.exception_object

                if state is not None and state.has_result:
                    return state.result

                if resolved.error_return is not RE_RAISE:
                    return resolved.error_return

                raise

            finally:
                # =================================
                # Stack cleanup with invariant check
                # =================================
                if state is not None and self._stack:
                    if self._stack[-1] is state:
                        self._stack.pop()
                    else:
                        self._handle_stack_corruption(state)
                        self._stack.clear()

        return wrapper

    return decorator