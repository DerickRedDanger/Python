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
import pandas as pd
import threading
import time
from pathlib import Path


# ============================================================
# Utility Functions
# ============================================================

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
    if mode == 'string':
        try:
            s = str(obj)
            return s if len(s) < 1000 else s[:1000] + '... [truncated]'
        except Exception as e:
            return f"<snapshot_error: string conversion failed ({e})>"
    raise ValueError("Invalid mode. Accepted: none, reference, shallowcopy, deepcopy, string.")


def arg_type(argument):
    """Return a list of argument types or name/type pairs for display."""
    if not argument:
        return "NoneType"
    if isinstance(argument, dict):
        return [(k, type(v).__name__) for k, v in argument.items()]
    if isinstance(argument, (list, tuple)):
        return [type(arg).__name__ for arg in argument]
    return [type(argument).__name__]

class BaseBuffer:
    """Base class for buffering logs before writing or merging."""
    def __init__(self, buffer_size=1000, auto_flush_interval=None):
        self.buffer = []
        self.buffer_size = buffer_size
        self.lock = threading.Lock()
        self._stop_event = threading.Event()

        if auto_flush_interval:
            self._start_auto_flush(auto_flush_interval)

    def log(self, record: dict):
        with self.lock:
            self.buffer.append(record)
            if len(self.buffer) >= self.buffer_size:
                self.flush()

    def flush(self):
        raise NotImplementedError

    def _start_auto_flush(self, interval):
        def run():
            while not self._stop_event.is_set():
                time.sleep(interval)
                with self.lock:
                    self.flush()
        threading.Thread(target=run, daemon=True).start()

    def stop_auto_flush(self):
        self._stop_event.set()


class MemoryBuffer(BaseBuffer):
    """In-memory DataFrame buffer."""
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
        """Efficiently merge DataFrames."""
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


class CSVBuffer(BaseBuffer):
    """CSV-backed buffer for persistent logging."""
    def __init__(self, csv_path="logs.csv", buffer_size=1000, auto_flush_interval=None, overwrite=False):
        super().__init__(buffer_size, auto_flush_interval)
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

        if overwrite and self.csv_path.exists():
            self.csv_path.unlink()  # remove existing file

        # create empty file if not exists
        if not self.csv_path.exists():
            with open(self.csv_path, "w", encoding="utf-8") as f:
                pass

    def flush(self):
        if not self.buffer:
            return
        df = pd.DataFrame(self.buffer)
        write_header = not self.csv_path.exists() or self.csv_path.stat().st_size == 0
        df.to_csv(self.csv_path, mode="a", header=write_header, index=False)
        self.buffer.clear()

    def get_dataframe(self):
        self.flush()
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            return pd.DataFrame()
        return pd.read_csv(self.csv_path)
    
    def clear(self, clear_file=True):
        """Clear memory buffer and optionally clear CSV file."""
        self.buffer.clear()
        if clear_file and os.path.exists(self.file_path):
            import os
            with open(self.file_path, "w") as f:
                f.truncate(0)

class Logger:
    def __init__(self, backend="memory", buffer_size=1000, csv_path="logs.csv", overwrite=False):
        """
        Initialize the logger with a backend:
        - 'memory': in-memory DataFrame logging
        - 'csv': persistent CSV logging
        """
        if backend == "memory":
            self.backend = MemoryBuffer(buffer_size=buffer_size)
        elif backend == "csv":
            self.backend = CSVBuffer(csv_path=csv_path, buffer_size=buffer_size, overwrite=overwrite)
        else:
            raise ValueError("Invalid backend. Choose 'memory' or 'csv'.")

    def log(self, record: dict):
        self.backend.log(record)

    def flush(self):
        self.backend.flush()

    def get_dataframe(self):
        return self.backend.get_dataframe()
    
    def clear(self, clear_file=True):
        """Clear the buffer (and file, if CSVBuffer)."""
        self.backend.clear() if not isinstance(self.backend, CSVBuffer) else self.backend.clear(clear_file)



# ============================================================
# Function Logger
# ============================================================

class FunctionLogger:
    """
    A configurable function logger that tracks calls, arguments, warnings, and errors.
    """

    LOG_MODE = {"error": 2, "warning": 1, "all": 0}

    def __init__(self, store_mode='reference',
                 arg_store_mode=None,
                 kwarg_store_mode=None,
                 result_store_mode=None,
                 log_level="warning",
                 default_error_return=None,
                 backend="memory", 
                 buffer_size=1000, 
                 csv_path="logs.csv", 
                 overwrite=False):
        
        if log_level not in self.LOG_MODE:
            raise ValueError(f"Invalid log_level: {log_level}. Choose from {list(self.LOG_MODE.keys())}")

        self.logs = Logger(backend=backend, buffer_size=buffer_size, csv_path=csv_path, overwrite=overwrite)
        self.faulty_args = []
        self.call_counter = defaultdict(int)
        self.store_mode = store_mode
        self.arg_store_mode = arg_store_mode or store_mode
        self.kwarg_store_mode = kwarg_store_mode or store_mode
        self.result_store_mode = result_store_mode or store_mode
        self.log_counter = 0
        self.log_level = log_level
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
                self.call_counter[func.__name__] += 1
                call_number = self.call_counter[func.__name__]
                parent_id, parent_call, parent_tag, depth = self.tracker_enter(func.__name__, call_number, tag)

                start_time = time.time()
                error = None
                result = None
                warnings_list = []

                # --- Capture warnings safely ---
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        error = traceback.format_exc()
                        result = self.handle_error_return(error_return, e)
                        self._record_faulty_args(func.__name__, call_number, tag,
                                                 parent_id, parent_call, parent_tag, depth,
                                                 args, kwargs, error)
                    finally:
                        for warn in w:
                            warnings_list.append({
                                "category": warn.category.__name__,
                                "message": str(warn.message),
                                "filename": getattr(warn, "filename", None),
                                "lineno": getattr(warn, "lineno", None)
                            })

                self.tracker_exit()

                duration = round(time.time() - start_time, 4)

                entry = {
                    "error": error,
                    "warnings": warnings_list,
                }

                if self._should_log(entry):
                    if not error:
                        self.log_counter += 1

                    log_entry = {
                        "id": self.log_counter,
                        "function": func.__name__,
                        "call": call_number,
                        "tag": tag,
                        "parent_id": parent_id,
                        "parent_call": parent_call,
                        "parent_tag": parent_tag,
                        "depth": depth,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                        "duration": duration,
                        "args type": arg_type(args),
                        "kwargs type": arg_type(kwargs),
                        "result type": arg_type(result),
                        "args": snapshot(args, arg_snap_mode or self.arg_store_mode),
                        "kwargs": snapshot(kwargs, kwarg_snap_mode or self.kwarg_store_mode),
                        "result": snapshot(result, result_snap_mode or self.result_store_mode),
                        "warnings": warnings_list,
                        "error": error,
                    }
                    self.logs.log(log_entry)

                return result
            return wrapper
        return decorator

    # ------------------------------------------------------------
    # Faulty Arguments Recorder
    # ------------------------------------------------------------
    def _record_faulty_args(self, func_name, call_number, tag,
                            parent_id, parent_call, parent_tag, depth,
                            args, kwargs, error):
        """Store information about calls that raised exceptions."""
        self.log_counter += 1
        self.faulty_args.append({
            "index": len(self.faulty_args),
            "id": self.log_counter,
            "function": func_name,
            "call": call_number,
            "tag": tag,
            "parent_id": parent_id,
            "parent_call": parent_call,
            "parent_tag": parent_tag,
            "depth": depth,
            "args": snapshot(args, mode='deepcopy'),
            "kwargs": snapshot(kwargs, mode='deepcopy'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "error": error,
        })

    # ------------------------------------------------------------
    # Log Level Filtering
    # ------------------------------------------------------------
    def _should_log(self, entry):
        lvl = self.LOG_MODE[self.log_level]
        if lvl == 2:
            return entry["error"] is not None
        if lvl == 1:
            return bool(entry["warnings"]) or entry["error"] is not None
        return True

    # ------------------------------------------------------------
    # Error Return Handler
    # ------------------------------------------------------------
    def handle_error_return(self, local_return=None, exc=None):
        chosen = local_return if local_return is not None else self.default_error_return

        if chosen == "raise":
            raise exc
        if callable(chosen):
            try:
                return chosen(exc)
            except Exception as inner_exc:
                err_msg = f"[Logger] Error in custom return callback: {inner_exc}"
                print(err_msg)
                self.logs.log({
                    "id": self.log_counter + 1,
                    "function": "<logger_callback>",
                    "error": err_msg,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                })
                return None
        return chosen

    # ------------------------------------------------------------
    # Call Context Tracker
    # ------------------------------------------------------------
    def tracker_enter(self, func_name, call_num, tag):
        parent_name, parent_call, parent_tag = self.tracker_stack[-1] if self.tracker_stack else (None, None, None)
        self.tracker_stack.append((func_name, call_num, tag))
        return parent_name, parent_call, parent_tag, len(self.tracker_stack) - 1

    def tracker_exit(self):
        if self.tracker_stack:
            self.tracker_stack.pop()

    # ------------------------------------------------------------
    # Accessor Methods
    # ------------------------------------------------------------
    def get_log(self):
        return list(self.logs)

    def clear(self, confirm=False):
        if confirm or input("Clear all logs? (y/N): ").lower() == "y":
            self.logs.clear()
            self.faulty_args.clear()
            self.log_counter = 0
            self.call_counter.clear()
            print("Logs cleared.")
        else:
            print("Clear aborted.")

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
