import logging
from logging.handlers import RotatingFileHandler

def create_log(
        log_filename: str, 
        max_log_size_bytes: int = 10 * 1024 * 1024, 
        backup_count: int = 5, 
        log_level=logging.DEBUG):
    """
    Create a rotating log with the given parameters and a stream handler for console output.

    Args:
        log_filename (str): The name of the log file.
        max_log_size_bytes (int): The maximum log file size in bytes before rotation.
        backup_count (int): The number of backup log files to keep.
        log_level (int): The logging level (default is logging.DEBUG).

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(log_filename)
    logger.setLevel(log_level)

    # Create a RotatingFileHandler for the log file
    file_handler = RotatingFileHandler(log_filename, maxBytes=max_log_size_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Create a StreamHandler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger