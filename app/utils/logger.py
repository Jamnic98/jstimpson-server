import logging


def get_logger():
    # Create a new logger
    log = logging.getLogger(__name__)
    # Set the logging level
    log.setLevel(logging.DEBUG)
    # Create a custom log message format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # Create a handler for the logger
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # Add the handler to the logger
    log.addHandler(stream_handler)
    return log


logger = get_logger()
