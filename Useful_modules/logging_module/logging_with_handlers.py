import logging

# Create a custom logger
logger = logging.getLogger()

# Clear previous handlers to avoid conflicts
logger.handlers.clear()

# Set the minimum logging level for the logger (applies to all handlers)
logger.setLevel(logging.DEBUG)

# Create handlers
file_handler = logging.FileHandler('app_with_handlers.log', mode='w')  # Log to a file
console_handler = logging.StreamHandler()  # Log to the console

# Set logging levels for each handler
file_handler.setLevel(logging.DEBUG)  # File logs everything (DEBUG and above)
console_handler.setLevel(logging.WARNING)  # Console only logs warnings and above
# obs:(critical > error > warning > info > debug)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Log messages at various levels
logger.debug("This is a DEBUG message")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")
logger.critical("This is a CRITICAL message")
