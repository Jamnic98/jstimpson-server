import logging


def get_logger():
    log = logging.getLogger(__name__)

    if not log.hasHandlers():  # Prevent duplicate handlers
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        log.addHandler(stream_handler)
        log.propagate = False  # Prevent duplicate logs

    return log

logger = get_logger()
