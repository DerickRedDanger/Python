"""
os Module - Operating System Interfaces

Introduction:
The 'os' module in Python provides functions to interact with the operating system, such as reading or writing to the filesystem, managing environment variables, and more.

Installation:
The os module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

import os

# 1. Get current working directory
print(f"Current working directory: {os.getcwd()}")

# 2. List files in a directory
print(f"Files in current directory: {os.listdir('.')}")

"""
Advanced Usage:
"""

# 1. Creating and removing directories
os.mkdir('new_directory')  # Creates a new directory
print("Created new_directory")
os.rmdir('new_directory')  # Removes the directory
print("Removed new_directory")

# 2. Working with environment variables
os.environ['MY_VARIABLE'] = '123'
print(f"MY_VARIABLE: {os.getenv('MY_VARIABLE')}")

"""
Real-World Example:
"""
# Walk through a directory and its subdirectories
for dirpath, dirnames, filenames in os.walk('.'):
    print(f"Found directory: {dirpath}")
    for file_name in filenames:
        print(f"File: {file_name}")
