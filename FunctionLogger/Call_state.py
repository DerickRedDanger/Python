        state = CallState(
            call_id=call_id,
            root_call_id=root_call_id,
            parent_call_id=parent_call_id,
            depth=depth,

            func_call_index=func_call_index,

            function_name=function_name,
            qualified_name=qualified_name,
            module_name=module_name,
            file_name=defined_file,
            def_line=defined_line,

            called_file=called_file,
            called_line=called_line,
            tag=resolved_tag,

            start_time_perf=perf_counter(),
            start_time_wall=time.time(),

            raised_exception=False,
            exception_object=None,
            traceback_str=None,

            warnings_captured=[],
            timeout_triggered=False,

            result=None,
            has_result=False,
            used_error_return=False,
        )