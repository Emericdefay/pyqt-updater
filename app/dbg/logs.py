import logging
import time

from updater.settings import DEBUG

def setup_logs():
    level = None
    if DEBUG:
        level = logging.DEBUG
    else:
        level = logging.INFO
    # Configurer le niveau de journalisation et le format des messages de log
    logging.basicConfig(filename='myapp.log',
                        level=level,
                        format='%(asctime)s %(levelname)s %(funcName)s %(message)s')


def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"Call {func.__name__}. Elapsed time: {elapsed_time:.2f} sec.")
            return result
        except Exception as e:
            logging.exception(f"{func.__name__}() Exception : {str(e)}")
            raise
    return wrapper