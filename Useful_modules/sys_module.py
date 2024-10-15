"""
sys Module - System-Specific Parameters and Functions

Introduction:
The 'sys' module provides access to some variables used or maintained by the interpreter and to functions that interact with the interpreter.

Installation:
The sys module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

import sys

# 1. Command-line arguments
print(f"Command-line arguments: {sys.argv}")

# 2. Get Python version
print(f"Python version: {sys.version}")

"""
Advanced Usage:
"""

# 1. Set a custom exit code
print("Exiting program with code 0")
# sys.exit(0)  # This will terminate the program, outputting 0 as the exit code

# 2. Redirecting stdout (standard output)
sys.stdout = open('sys_Module_output.txt', 'w')
print("This will be written to output.txt")

"""
Real-World Example:
"""
# Manage memory using sys.getsizeof
x = [i for i in range(1000)]
print(f"Memory size of list: {sys.getsizeof(x)} bytes")
