"""Performance profiling helpers for Dream AI evolution."""

from __future__ import annotations

import time
import tracemalloc
from typing import Any, Callable, Dict


class Profiler:
    """Measure execution time and memory usage."""

    def measure_execution_time(self, func: Callable, *args: Any, **kwargs: Any) -> float:
        """Run a function and return execution time in milliseconds."""
        start = time.perf_counter()
        try:
            func(*args, **kwargs)
        finally:
            end = time.perf_counter()
        return (end - start) * 1000.0

    def measure_memory_usage(self) -> Dict[str, int]:
        """Report current and peak memory usage using tracemalloc."""
        tracemalloc.start()
        try:
            current, peak = tracemalloc.get_traced_memory()
            return {"current_bytes": int(current), "peak_bytes": int(peak)}
        finally:
            tracemalloc.stop()








