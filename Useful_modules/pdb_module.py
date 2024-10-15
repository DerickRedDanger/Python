"""
pdb Module - Python Debugger

Introduction:
The 'pdb' module is Python’s built-in debugger that lets you set breakpoints, inspect variables, step through code, and interactively debug your scripts.

Installation:
The pdb module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

import pdb

def faulty_function():
    x = 5
    y = 0
    pdb.set_trace()  # Start debugging here
    return x / y

# Run the function to trigger pdb debugger
# faulty_function()  # Uncomment to test

"""
Advanced Usage:
"""

# 1. Setting breakpoints without pdb.set_trace()
breakpoint()  # This is equivalent to pdb.set_trace() in Python 3.7+

# 2. Using pdb in the terminal:
# python -m pdb my_script.py  # This will start the debugger on script execution

"""
Real-World Example:
"""
# Debugging a loop
for i in range(5):
    pdb.set_trace()
    print(f"Processing {i}")
    
"""
debugger commands:
n (next): Move to the next line of code.
c (continue): Continue execution until the next breakpoint.
p variable_name: Print the value of a variable.
l (list): Show the current location in the code.
q (quit): Exit the debugger.
b (break): Set a breakpoint at a specified line.
s (step): Step into a function call.
r (return): Continue execution until the current function returns.
"""