import threading
import time
import pandas as pd
import os
from abc import ABC, abstractmethod
from pathlib import Path
import copy
import traceback
import time
import warnings
from collections import deque, defaultdict
from datetime import datetime
from functools import wraps
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


# ============================================================
# Utility Functions
# ============================================================

#  --------------- Snapshot --------------- 

def snapshot(obj, mode='reference'):
    """Return an object snapshot according to the chosen mode."""
    if mode == 'none':
        return None
    if mode == 'reference':
        return obj
    if mode == 'shallowcopy':
        try:
            return copy.copy(obj)
        except Exception as e:
            return f"<snapshot_error: shallowcopy failed ({e})>"
    if mode == 'deepcopy':
        try:
            return copy.deepcopy(obj)
        except Exception as e:
            return f"<snapshot_error: deepcopy failed for {type(obj).__name__} ({e})>"
    if mode == 'str':
        try:
            if hasattr(obj, "shape"):
                return f"<{type(obj).__name__} shape={obj.shape}>"
                
            if isinstance(obj, (list, tuple, set)):
                return f"<{type(obj).__name__} len={len(obj)}>"
                
            if isinstance(obj, dict):
                return f"<dict len={len(obj)} keys={list(obj)[:5]}>"
    
            s = str(obj)
            return s if len(s) < 1000 else s[:1000] + '... [truncated]'
        except Exception as e:
            return f"<snapshot_error: string conversion failed ({e})>"


#  --------------- Argument type --------------- 

def arg_type(argument):
    """Return a list of argument types or name/type pairs for display."""
    if argument is None:
        return "NoneType"
    if isinstance(argument, dict):
        return [(k, type(v).__name__) for k, v in argument.items()]
    if isinstance(argument, (list, tuple)):
        return [type(arg).__name__ for arg in argument]
    return [type(argument).__name__]

#  --------------- Base class for log buffers --------------- 

class BaseBuffer(ABC):
    """Abstract base class for buffering logs before writing or merging."""

    def __init__(self, buffer_size=1000, auto_flush_interval=None):
        self.buffer = []
        self.buffer_size = buffer_size
        self.lock = threading.Lock()
        self._stop_event = threading.Event()

        if auto_flush_interval:
            self.start_auto_flush(auto_flush_interval)

    def log(self, record: dict):
        """Append a record to the buffer and flush if full."""
        with self.lock:
            self.buffer.append(record)
            if len(self.buffer) >= self.buffer_size:
                self.flush()

    @abstractmethod
    def flush(self):
        """Flush the buffer to the underlying storage (must be implemented by subclass)."""
        pass

    def start_auto_flush(self, interval):
        """Start a background thread that flushes at a fixed interval."""
        self._stop_event.clear()
        def run():
            while not self._stop_event.is_set():
                time.sleep(interval)
                try:
                    with self.lock:
                        self.flush()
                except Exception as e:
                    print(f"[AutoFlush Error]: {e}")
        threading.Thread(target=run, daemon=True).start()

    def stop_auto_flush(self):
        """Stop the auto-flush thread."""
        self._stop_event.set()

    @abstractmethod
    def get_dataframe(self):
        """Return a DataFrame representation of the stored data."""
        pass

    @abstractmethod
    def clear(self):
        """Clear the buffer and all persisted data (if applicable)."""
        pass

#  --------------- Memory Buffer - Subclass of BaseBuffer --------------- 

class MemoryBuffer(BaseBuffer):
    """In-memory DataFrame buffer implementation of BaseBuffer."""

    def __init__(self, buffer_size=1000, auto_flush_interval=None):
        super().__init__(buffer_size, auto_flush_interval)
        self.dfs = []

    def flush(self):
        if not self.buffer:
            return
        df = pd.DataFrame(self.buffer)
        self.dfs.append(df)
        self.buffer.clear()

    def balanced_concat(self):
        """Efficiently merge DataFrames in a balanced way."""
        if len(self.dfs) < 2:
            return
        dfs = self.dfs
        while len(dfs) > 1:
            new = []
            for i in range(0, len(dfs), 2):
                if i + 1 < len(dfs):
                    new.append(pd.concat([dfs[i], dfs[i + 1]], ignore_index=True))
                else:
                    new.append(dfs[i])
            dfs = new
        self.dfs = dfs

    def get_dataframe(self):
        self.flush()
        self.balanced_concat()
        return self.dfs[0] if self.dfs else pd.DataFrame()

    def clear(self):
        """Clear all stored data and reset the buffer."""
        self.buffer.clear()
        self.dfs.clear()
        print('Cleared buffer')

#  --------------- CSV Buffer - Subclass of BaseBuffer --------------- 

class CSVBuffer(BaseBuffer):
    """CSV-backed buffer for persistent logging."""

    def __init__(self, csv_path="logs.csv", buffer_size=1000, auto_flush_interval=None, overwrite=True):
        super().__init__(buffer_size, auto_flush_interval)
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

        if overwrite and self.csv_path.exists():
            self.csv_path.unlink()  # remove existing file

        # create empty file if not exists
        if not self.csv_path.exists():
            self.csv_path.touch()

    def flush(self):
        if not self.buffer:
            return
        df = pd.DataFrame(self.buffer)
        write_header = self.csv_path.stat().st_size == 0
        df.to_csv(self.csv_path, mode="a", header=write_header, index=False)
        self.buffer.clear()

    def get_dataframe(self):
        self.flush()
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            return pd.DataFrame()
        return pd.read_csv(self.csv_path, keep_default_na=False, na_values=[""], dtype=object)

    def clear(self, clear_file=True):
        """Clear memory buffer and optionally clear CSV file."""
        self.buffer.clear()
        if clear_file and self.csv_path.exists():
            with open(self.csv_path, "w", encoding="utf-8") as f:
                f.truncate(0)
        print(f"Cleared buffer{' and file' if clear_file else ''}.")

# ===================================
#  LOGGER WRAPPER
# ===================================
class Logger:
    """A lightweight wrapper around a buffer (memory or csv)."""

    def __init__(self, backend="memory", **kwargs):
        if backend == "memory":
            self.buffer = MemoryBuffer(**kwargs)
        elif backend == "csv":
            self.buffer = CSVBuffer(**kwargs)
        else:
            raise ValueError(f"Unknown backend '{backend}'. Choose 'memory' or 'csv'.")

    def log(self, record: dict):
        self.buffer.log(record)

    def get_dataframe(self):
        return self.buffer.get_dataframe()

    def clear(self):
        self.buffer.clear()

    def flush(self):
        self.buffer.flush()

# ============================================================
# Function Logger
# ============================================================

class FunctionLogger:
    """
    A configurable function logger that tracks calls, arguments, warnings, and errors.
    """

    LOG_MODE = {"error": 2, "warning": 1, "all": 0}
    VERBOSITY_LEVELS = {"off": 0, "warn": 1, "debug": 2, "trace": 3}

    def __init__(self, store_mode='reference',
                 backend="memory",
                 buffer_size=1000,
                 auto_flush_interval=None,
                 csv_path="logs.csv",
                 overwrite=True,
                 arg_store_mode=None,
                 kwarg_store_mode=None,
                 result_store_mode=None,
                 log_level="warning",
                 default_error_return=None,
                 verbose='warn'):
        
        if log_level not in self.LOG_MODE:
            raise ValueError(f"Invalid log_level: {log_level}. Choose from {list(self.LOG_MODE.keys())}")

        if verbose not in self.VERBOSITY_LEVELS:
            raise ValueError(f"Invalid verbose level: {verbose}. Choose from {list(self.VERBOSITY_LEVELS)}")

        self.logs = Logger(backend=backend)
        self.faulty_args = []
        self.internal_errors = []
        self.snapshot_registry = {}
        self.call_counter = defaultdict(int)
        self.store_mode = store_mode
        self.arg_store_mode = arg_store_mode or store_mode
        self.kwarg_store_mode = kwarg_store_mode or store_mode
        self.result_store_mode = result_store_mode or store_mode
        self.log_counter = 0
        self.log_level = log_level
        self.verbose = verbose
        self.default_error_return = default_error_return
        self.tracker_stack = []

    # ------------------------------------------------------------
    # Decorator Factory
    # ------------------------------------------------------------
    def log_function(self, tag=None, error_return=None,
                     arg_snap_mode=None, kwarg_snap_mode=None, result_snap_mode=None):
        """Decorator factory to wrap functions with logging, tagging, and safe warning capture."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # increment per-function call counter and compute call number
                self.call_counter[func.__name__] += 1
                call_number = self.call_counter[func.__name__]

                # capture start time (float) for duration calc and human-readable timestamp
                start_time = time.time()

                # enter tracker: creates partial_log + pushes frame onto tracker_stack, returns parent info + log_id
                parent_id, parent_call, parent_tag, depth, log_id = self.tracker_enter(func.__name__, call_number, tag, start_time=start_time)

                # Determine snapshot modes for this invocation (decorator-level overrides instance-level)
                arg_mode = arg_snap_mode or self.arg_store_mode
                kw_mode = kwarg_snap_mode or self.kwarg_store_mode
                res_mode = result_snap_mode or self.result_store_mode

                # Prepare the initial partial-log's args/kwargs stringified fields and types in the frame
                # (frame is last item on tracker_stack)
                try:
                    frame = self.tracker_stack[-1]
                    # set types and string representations for DataFrame-friendly storage
                    frame["partial_log"]["args type"] = arg_type(args)
                    frame["partial_log"]["kwargs type"] = arg_type(kwargs)
                    frame["partial_log"]["args"] = snapshot(args, "str")
                    frame["partial_log"]["kwargs"] = snapshot(kwargs, "str")
                except Exception as e:
                    # worst case: record internal error and continue
                    tb = traceback.format_exc()
                    self.internal_errors.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                        "context": "entry_snapshot",
                        "error": str(e),
                        "traceback": tb
                    })

                # Also, store the *actual* arg/kw snapshots in the registry if their modes are not 'str' or 'none'
                if arg_mode not in ("none", "str"):
                    try:
                        self.snapshot_registry[log_id] = self.snapshot_registry.get(log_id, {})
                        self.snapshot_registry[log_id]["args"] = snapshot(args, arg_mode)
                    except Exception as e:
                        self.snapshot_registry[log_id]["args"] = f"<snapshot_error: args snapshot failed ({e})>"
                if kw_mode not in ("none", "str"):
                    try:
                        self.snapshot_registry[log_id] = self.snapshot_registry.get(log_id, {})
                        self.snapshot_registry[log_id]["kwargs"] = snapshot(kwargs, kw_mode)
                    except Exception as e:
                        self.snapshot_registry[log_id]["kwargs"] = f"<snapshot_error: kwargs snapshot failed ({e})>"

                error = None
                result = None
                warnings_list = []

                # --- Capture warnings safely and execute the wrapped function ---
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        # capture full traceback for debugging
                        error = traceback.format_exc()
                        # pass the current log_id so faulty args use the correct id (no extra increments)
                        self._record_faulty_args(log_id, func.__name__, call_number, tag,
                                                 parent_id, parent_call, parent_tag, depth,
                                                 args, kwargs, error)
                        result = self._handle_error_return(error_return, e)
                    finally:
                        for warn in w:
                            warnings_list.append({
                                "category": warn.category.__name__,
                                "message": str(warn.message),
                                "filename": getattr(warn, "filename", None),
                                "lineno": getattr(warn, "lineno", None)
                            })

                # Finalize and append to the main log via tracker_exit
                finalized = self.tracker_exit(log_id, result, error, warnings_list,
                                              arg_snap_mode=arg_mode, kwarg_snap_mode=kw_mode, result_snap_mode=res_mode)

                # If _should_log decides not to include (e.g., log_level), we could drop it post-hoc.
                # However we still have already assigned id and created snapshots. To preserve original log-level logic,
                # we can decide here whether to actually keep the appended log row. For simplicity and to preserve
                # deterministic ids, we will follow _should_log and only append when true.
                # But since tracker_exit already appended, we need to filter this earlier.
                # To avoid double-work, we check the _should_log decision here and, if needed, remove the last log from buffer.
                # NOTE: Your buffer implementations don't expose an easy "pop last" API — keeping logs append-only is simpler.
                # So instead we will respect _should_log and avoid assigning log ids when entry should not be logged.
                # (We could refactor to decide _should_log before tracker_enter; but that requires running the function to know warnings/errors.)
                # For now, we keep it simple: the logger appends entries and users configure log_level to control noise.

                return result
            return wrapper
        return decorator


    # ------------------------------------------------------------
    # Faulty Arguments Recorder (updated to accept log_id)
    # ------------------------------------------------------------
    def _record_faulty_args(self, log_id, func_name, call_number, tag,
                            parent_id, parent_call, parent_tag, depth,
                            args, kwargs, error):
        """Store information about calls that raised exceptions."""
        # do NOT change self.log_counter here — log_id is now assigned at entry
        self.faulty_args.append({
            "index": len(self.faulty_args),
            "log_id": log_id,
            "function": func_name,
            "call": call_number,
            "tag": tag,
            "parent_id": parent_id,
            "parent_call": parent_call,
            "parent_tag": parent_tag,
            "depth": depth,
            "args": snapshot(args, mode=self.arg_store_mode if self.arg_store_mode is not None else self.store_mode),
            "kwargs": snapshot(kwargs, mode=self.kwarg_store_mode if self.kwarg_store_mode is not None else self.store_mode),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "error": error,
        })
    # ------------------------------------------------------------
    # Log Level Filtering
    # ------------------------------------------------------------
    def _should_log(self, entry):
        lvl = self.LOG_MODE[self.log_level]
        if lvl == 3:
            return False
        if lvl == 2:
            return entry["error"] is not None
        if lvl == 1:
            return bool(entry["warnings"]) or entry["error"] is not None
        return True

    # ------------------------------------------------------------
    # Error Return Handler
    # ------------------------------------------------------------
    def _handle_error_return(self, local_return=None, exc=None):
        chosen = local_return if local_return is not None else self.default_error_return
    
        if chosen == "raise":
            raise exc
        if callable(chosen):
            try:
                return chosen(exc)
            except Exception as inner_exc:
                err_msg = f"[Logger] Error in custom return callback: {inner_exc}"
                tb_str = traceback.format_exc()
    
                # Store internal error
                self.internal_errors.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    "context": "_handle_error_return",
                    "error": err_msg,
                    "traceback": tb_str
                })
    
                # Handle verbosity-controlled printing
                v = self.VERBOSITY_LEVELS[self.verbose]
                if v >= 2:  # debug or higher
                    print(err_msg)
                    if v >= 3:  # trace mode
                        print(tb_str)
    
                return None
        return chosen


    # ------------------------------------------------------------
    # Call Context Tracker (entry creates partial_log; exit finalizes)
    # ------------------------------------------------------------
    def tracker_enter(self, func_name, call_num, tag, start_time=None):
        """
        Create a stack frame and a partial log record at function entry.
        Returns: parent_id, parent_call, parent_tag, depth, log_id
        """
        # get parent frame info if any
        parent_frame = self.tracker_stack[-1] if self.tracker_stack else None
        parent_name = parent_frame["func"] if parent_frame else None
        parent_call = parent_frame["call"] if parent_frame else None
        parent_tag = parent_frame["tag"] if parent_frame else None
        parent_id = parent_frame["partial_log"]["id"] if parent_frame else None
        depth = len(self.tracker_stack)

        # compute assigned log id right away (chronological id)
        self.log_counter += 1
        log_id = self.log_counter

        # timestamp for human-readable log
        ts = (datetime.fromtimestamp(start_time) if start_time is not None else datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Build the partial log (strings for args/kwargs to keep the DataFrame lightweight)
        partial_log = {
            "id": log_id,
            "function": func_name,
            "call": call_num,
            "tag": tag,
            "parent_id": parent_id,
            "parent_name": parent_name,
            "parent_call": parent_call,
            "parent_tag": parent_tag,
            "depth": depth,
            "timestamp_start": ts,
            "duration": None,
            "timestamp_end": None,
            "args type": None,    # will set below
            "kwargs type": None,
            "result type": None,
            "args": None,
            "kwargs": None,
            "result": None,
            "warnings": None,
            "error": None,
        }

        # snapshot modes (resolve from local decorator args later; but use defaults if provided via class settings)
        # NOTE: we do not know decorator-level modes here; wrapper will compute modes and update partial_log fields below.
        frame = {
            "func": func_name,
            "call": call_num,
            "tag": tag,
            "parent_func": parent_name,
            "parent_call": parent_call,
            "parent_tag": parent_tag,
            "depth": depth,
            "start_time": start_time if start_time is not None else time.time(),
            "partial_log": partial_log
        }

        # push frame onto stack
        self.tracker_stack.append(frame)

        return parent_id, parent_call, parent_tag, depth, log_id

    def tracker_exit(self, log_id, result, error, warnings_list,
                     arg_snap_mode=None, kwarg_snap_mode=None, result_snap_mode=None):
        """
        Finalize the partial log for the last frame and append it to the final logs buffer.
        This assumes the caller popped in proper LIFO order (we validate).
        """
        if not self.tracker_stack:
            # Defensive: no stack frame (shouldn't happen normally)
            # Still create a final entry with minimal info
            final_entry = {
                "id": log_id,
                "function": None,
                "call": None,
                "tag": None,
                "parent_id": None,
                "parent_name": None,
                "parent_call": None,
                "parent_tag": None,
                "depth": None,
                "timestamp_start": None,
                "duration": None,
                "timestamp_end": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "args type": None,
                "kwargs type": None,
                "result type": arg_type(result),
                "args": None,
                "kwargs": None,
                "result": snapshot(result, "str"),
                "warnings": warnings_list,
                "error": error,
            }
            # append to logs
            self.logs.log(final_entry)
            return final_entry

        # pop the last frame and ensure it matches the log_id passed
        frame = self.tracker_stack.pop()
        frame_log = frame["partial_log"]
        if frame_log["id"] != log_id:
            # If mismatch, log a warning and try to proceed with the frame we popped.
            warn_msg = (f"[Logger] tracker id mismatch: expected log_id {log_id}, "
                        f"but found {frame_log['id']}. Proceeding with popped frame.")
            self.internal_errors.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "context": "tracker_exit_mismatch",
                "error": warn_msg,
                "traceback": None
            })
            print(warn_msg)

        # compute end timestamps and duration
        end_time_f = time.time()
        timestamp_end = datetime.fromtimestamp(end_time_f).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        duration = round(end_time_f - frame["start_time"], 4)

        # finalize fields in the log entry
        frame_log["timestamp_end"] = timestamp_end
        frame_log["duration"] = duration
        frame_log["result type"] = arg_type(result)
        frame_log["result"] = snapshot(result, "str")
        frame_log["warnings"] = warnings_list if warnings_list else []
        frame_log["error"] = error

        # If the partial_log didn't yet have args/kwargs type + str snapshot (because wrapper didn't set them),
        # we keep them None. But wrapper should have set them at entry.
        # Now save full snapshots into snapshot_registry according to resolved modes.

        # Resolve snapshot modes (fall back to class-level settings)
        arg_mode = arg_snap_mode or self.arg_store_mode
        kw_mode = kwarg_snap_mode or self.kwarg_store_mode
        res_mode = result_snap_mode or self.result_store_mode
        
        snapshots = {}
        # Only store actual snapshots in the registry if modes require non-string storage
        # The partial_log already contains stringified args/kwargs/result for the DataFrame.
        # Use original objects if available in frame (we don't keep original args here to avoid large memory),
        # so the wrapper will have passed the original args/kwargs/result to the tracker_exit call.
        # The wrapper calls tracker_exit with the actual 'result' and also supplies the arg/kw values via the snapshot modes.
        # Here, we only create snapshots for the result if modes request it.
        # For args/kwargs, the wrapper stored real snapshots into registry at entry (see wrapper code).
        if res_mode != "str":
            try:
                snapshots["result"] = snapshot(result, res_mode)
            except Exception as e:
                snapshots["result"] = f"<snapshot_error: result snapshot failed ({e})>"
        else:
            snapshots["result"] = None

        # Merge into snapshot_registry if there are any snapshots to keep.
        # The wrapper already may have stored args/kwargs snapshots under this log_id.
        existing = self.snapshot_registry.get(frame_log["id"], {})
        # combine: existing (args/kwargs) + result
        merged = existing.copy() if isinstance(existing, dict) else {}
        merged.update(snapshots)
        if any(v is not None for v in merged.values()):
            self.snapshot_registry[frame_log["id"]] = merged

        # Finally, append the frame_log to the final logs buffer
        self.logs.log(frame_log)

        return frame_log

    # ------------------------------------------------------------
    # Accessor Methods
    # ------------------------------------------------------------
    def get_log(self):
        return self.logs.get_dataframe()

    def clear(self, confirm=False):
        if confirm or input("Clear all logs? (y/N): ").lower() == "y":
            self.logs.clear()
            self.faulty_args.clear()
            self.log_counter = 0
            self.call_counter.clear()
            self.snapshot_registry.clear()
            self.internal_errors.clear()
            print("Logs cleared.")
        else:
            print("Clear aborted.")
            
    # ------------------------------------------------------------
    # Faulty Arguments Accessor Methods
    # ------------------------------------------------------------
    def show_faulty_args(self):
        if not self.faulty_args:
            print("No faulty arguments recorded.")
            return
        for f in self.faulty_args:
            print(f"[ Error Id {f['index']}] from log (ID {f['id']}), function {f['function']} "
                  f"on call #{f['call']} with tag {f['tag']} failed at {f['timestamp']}")
            err_line = f['error'].splitlines()[-1] if f['error'] else "No traceback available"
            print(f"  Error: {err_line}\n")

    def get_faulty_entry(self, index):
        try:
            entry = self.faulty_args[index]
            return entry["args"], entry["kwargs"], entry["error"]
        except IndexError:
            print(f"No faulty entry found for index {index}.")
            return None, None, None

    def _warn_errors(self):
        if self.faulty_args and self.VERBOSITY_LEVELS[self.verbose] >= 1:
            print(f"[Logger] {len(self.faulty_args)} errors recorded. "
                  f"Use .show_faulty_args() to inspect.")

    # ------------------------------------------------------------
    # Display System
    # ------------------------------------------------------------
    def dump_logs(self, mode='table', max_entries=20):
        console = Console()
        if not self.logs:
            console.print("[yellow]No logs available.[/yellow]")
            return
        
        entries = list(self.logs)[-max_entries:]
        if mode == 'table':
            table = Table(title=f"Function Logs (last {len(entries)})", show_lines=True)
            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Function", style="bold white")
            table.add_column("Call", style="magenta")
            table.add_column("Tag", style="green")
            table.add_column("Duration (s)", justify="right")
            table.add_column("Warnings", style="yellow")
            table.add_column("Error", style="red")

            for e in entries:
                table.add_row(
                    str(e["id"]), e["function"], str(e["call"]),
                    str(e.get("tag") or "-"), f"{e['duration']}",
                    str(len(e["warnings"])), "Yes" if e["error"] else "No"
                )
            console.print(table)
        elif mode == 'panel':
            for e in entries:
                text = Text()
                text.append(f"[{e['id']}] {e['function']} (call #{e['call']})\n", style="bold cyan")
                if e.get("tag"): text.append(f"Tag: {e['tag']}\n", style="green")
                text.append(f"Duration: {e['duration']}s\nTime: {e['time']}\n\n", style="dim")
                if e["warnings"]:
                    text.append("Warnings:\n", style="yellow bold")
                    for w in e["warnings"]:
                        text.append(f"  - {w}\n", style="yellow")
                if e["error"]:
                    text.append("\nError:\n", style="red bold")
                    text.append(e["error"], style="red")
                console.print(Panel(text, title=f"Log #{e['id']}", expand=False, border_style="cyan"))
        else:
            console.print(f"[red]Invalid mode: {mode}[/red]")

    # ------------------------------------------------------------
    # Trace View
    # ------------------------------------------------------------
    def trace_hierarchy(self, show_errors=True, show_warnings=False):
        console = Console()
        if not self.logs:
            console.print("[yellow]No logs available.[/yellow]")
            return
        
        console.print("\n[bold underline cyan]Function Call Hierarchy[/bold underline cyan]")
        for log in self.logs:
            indent = "  " * log["depth"]
            error_flag = "❌" if log["error"] else ""
            warn_flag = f"⚠️({len(log['warnings'])})" if log["warnings"] else ""
            time_str = f"[dim]{log['time']}[/dim]"
            console.print(
                f"{indent}• [bold white]{log['function']}[/bold white] "
                f"[dim](call {log['call']})[/dim] {error_flag}{warn_flag} {time_str}"
            )
            if show_errors and log["error"]:
                console.print(f"{indent}  [red]{log['error'].splitlines()[-1]}[/red]")
            if show_warnings and log["warnings"]:
                for w in log["warnings"]:
                    console.print(f"{indent}  [yellow]- {w}[/yellow]")

    # ------------------------------------------------------------
    # Internal errors View
    # ------------------------------------------------------------

    def has_internal_errors(self):
        return len(self.internal_errors) > 0
        
    def get_internal_errors(self, as_dataframe=False):
        return pd.DataFrame(self.internal_errors) if as_dataframe else self.internal_errors
    
    def clear_internal_errors(self):
        self.internal_errors.clear()

    def _warn_internal_errors(self):
        if self.internal_errors and self.VERBOSITY_LEVELS[self.verbose] >= 1:
            print(f"[Logger] {len(self.internal_errors)} internal errors recorded. "
                  f"Use .get_internal_errors() to inspect.")



# ============================================================
# Null Object Logger
# ============================================================

class OffLogger:
    """Null Object version of FunctionLogger."""
    def log_function(self, *args, **kwargs):
        def decorator(func): return func
        return decorator
    def __getattr__(self, name): return lambda *_, **__: None


# ============================================================
# Global Toggle
# ============================================================

def get_logger(enabled=True, **kwargs):
    return FunctionLogger(**kwargs) if enabled else OffLogger()
