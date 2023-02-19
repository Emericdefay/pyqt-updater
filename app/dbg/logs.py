import logging
from datetime import datetime
import time
import os

from updater.settings import DEBUG, APP_NAME


def setup_logs():
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


def log_exceptions(func):
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
