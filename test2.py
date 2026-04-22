import time
import threading
import pandas as pd
from abc import ABC, abstractmethod
from pathlib import Path
import functools


# ===================================
#  BUFFER SYSTEM (your ABC version)
# ===================================
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


class CSVBuffer(BaseBuffer):
    """CSV-backed buffer for persistent logging."""

    def __init__(self, csv_path="logs.csv", buffer_size=1000, auto_flush_interval=None, overwrite=False):
        super().__init__(buffer_size, auto_flush_interval)
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv_path.touch(exist_ok=True)

        if overwrite and self.csv_path.exists():
            self.csv_path.unlink()
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
        return pd.read_csv(self.csv_path)

    def clear(self, clear_file=True):
        """Clear memory buffer and optionally clear CSV file."""
        self.buffer.clear()
        if clear_file and self.csv_path.exists():
            self.csv_path.write_text("")


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


# ===================================
#  FUNCTION LOGGER
# ===================================
class FunctionLogger:
    """Logs function calls, execution time, and optionally return values."""

    def __init__(self, backend="memory", **kwargs):
        self.logger = Logger(backend=backend, **kwargs)

    def log_function(self, log_return=False):
        """Decorator to log function calls with timing."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()

                record = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "function": func.__name__,
                    "execution_time": round(end - start, 6),
                    "args": str(args),
                    "kwargs": str(kwargs),
                }
                if log_return:
                    record["return"] = result

                self.logger.log(record)
                return result
            return wrapper
        return decorator

    def get_dataframe(self):
        return self.logger.get_dataframe()

    def clear(self):
        self.logger.clear()

    def flush(self):
        self.logger.flush()
