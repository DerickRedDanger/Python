import logging

"""
logging Module - Tracking Events in Code

Introduction:
The 'logging' module provides a flexible framework for emitting log messages from Python programs. It is especially useful for tracking the flow and state of applications during runtime.

Installation:
The logging module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

# Once basicConfig is called in the current session, subsequent calls have no effect.
# We need to remove the previous handlers using logging.getLogger().handlers.clear() before calling basicConfig again.

# Clear any existing handlers to avoid conflicts from previous basicConfig calls
logging.getLogger().handlers.clear()

# Set up basic logging configuration
logging.basicConfig(
    filename='app.log',           # Log messages will be written to app.log, delete to print it to the terminal
    filemode='w',                 # specifies the mode to load the file, 'w' for Overwrite the log file each time the program runs, 'a' for append to file
    level=logging.DEBUG,          # Log messages at DEBUG level and above(critical > error > warning > info > debug)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Set the format for log messages. time - message level - message
)

# Log messages at various levels
logging.debug("This is a DEBUG message")
logging.info("This is an INFO message")
logging.warning("This is a WARNING message")
logging.error("This is an ERROR message")
logging.critical("This is a CRITICAL message")

# 1. Log an exception in a real program
try:
    1 / 0
except ZeroDivisionError as e:
    logging.error("Exception occurred", exc_info=True)
