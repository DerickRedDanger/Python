"""
traceback Module - Print and Format Tracebacks

Introduction:
The 'traceback' module provides utilities for extracting, formatting, and printing information about exceptions in Python.

Installation:
The traceback module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

import traceback

# 1. Catch and print the traceback
try:
    1 / 0
except ZeroDivisionError:
    print("An error occurred")
    print(traceback.format_exc())

"""
Advanced Usage:
"""

# 1. Write traceback to a file
try:
    raise ValueError("An example exception")
except ValueError:
    with open("error_log.txt", "w") as f:
        f.write(traceback.format_exc())

"""
Real-World Example:
"""
# 1. Creating detailed error logs
def faulty():
    try:
        1 / 0
    except ZeroDivisionError:
        with open("detailed_log.txt", "w") as log_file:
            log_file.write(traceback.format_exc())

faulty()  # Uncomment to generate the error log
