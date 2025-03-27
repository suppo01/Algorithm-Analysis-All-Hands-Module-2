"""Timing context manager for profiling code."""

import contextlib
from time import perf_counter
from typing import Generator, List, Tuple

from rich.console import Console

# list to store performance data
performance_data: List[Tuple[str, float]] = []


@contextlib.contextmanager
def timer(
    context: str = "Time Overhead Measurement (ms)",
) -> Generator[None, None, None]:
    """Timing context manager for profiling code."""
    # start the timer
    start_time = perf_counter()
    # yield control back to the context manager's caller
    yield
    # stop the timer
    end_time = perf_counter()
    # calculate the duration of the code block
    duration = (end_time - start_time) * 1000
    performance_data.append((context, duration))


def output_performance_data(console: Console, label: str) -> None:
    """Output the saved performance data."""
    for context, duration in performance_data:
        console.print()
        console.print(f"{label} {context}: {duration:.2f} ms")
