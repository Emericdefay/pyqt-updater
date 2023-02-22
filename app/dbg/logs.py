import logging
from datetime import datetime
import time
import os
import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

from updater.settings import DEBUG


def setup_logs():
    """
    Configures logging for the application. Logs are saved in a 'logs' directory
    with the filename format: 'YYYY-MM-DD_HHhMMmSSs.log'. The logging level is set
    to 'DEBUG' if the global 'DEBUG' variable is set to True, or 'INFO' otherwise.
    The logs are written to a file and to the standard output/error streams.

    Returns:
        None
    """
    level = None
    if DEBUG:
        level = logging.DEBUG
    else:
        level = logging.INFO
    date = datetime.utcnow().strftime('%Y-%m-%d_%Hh%Mm%Ss')
    path = os.path.dirname(os.path.dirname(__file__))
    log_folder = 'logs'
    log_file = f'{date}.log'
    if not os.path.exists(os.path.join(path, log_folder)):
        os.mkdir(os.path.join(path, log_folder))
    full_path = os.path.join(path, log_folder, log_file)
    # Configurer le niveau de journalisation et le format des messages de log
    logging.basicConfig(
        filename=full_path,
        level=level,
        format='%(asctime)s %(levelname)s %(funcName)s %(message)s'
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = TimedRotatingFileHandler(full_path, when="midnight", interval=1, encoding='utf8')
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    sys.stdout = LoggerWriter(logging.debug)
    sys.stderr = LoggerWriter(logging.warning)


def log_exceptions(func):
    """
    A decorator function that logs any exceptions that occur during the decorated function's
    execution. The log message includes the function name, the elapsed time of the function
    call, and any exception that was raised.

    Args:
        func (callable): The function being decorated.

    Returns:
        callable: A wrapper function that logs any exceptions and re-raises them.
    """
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"Call {func.__name__: <20}. Elapsed time: {elapsed_time:.2f} sec.")
            return result
        except Exception as e:
            logging.exception(f"{func.__name__}() Exception : {str(e)}")
            raise
    return wrapper


class LoggerWriter:
    """
    A class that redirects standard output/error streams to the logging system.
    It allows messages written to the standard output/error streams to be captured
    and logged by the logging module.

    Args:
        level (logging.Level): The logging level to use for the captured messages.

    Attributes:
        level (logging.Level): The logging level to use for the captured messages.

    Methods:
        write(message): Writes a message to the logging system.
        flush(): Flushes the logger to ensure all messages have been processed.
    """
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message != '\n':
            self.level(message)

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)
