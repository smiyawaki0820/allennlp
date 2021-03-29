import re
import datetime

from src.utils.logger import logger

BLUE = '\033[34m'
END = '\033[0m'

def timer(tag):
    def _timer(func):
        def wrapper(*args, **kwargs):
            logger.info(BLUE + f'|--> START: {tag}' + END)
            start = datetime.datetime.now()
            result = func(*args, **kwargs)
            end = datetime.datetime.now()
            logger.info(f'| TIME: {end-start}')
            logger.info(BLUE + f'|--> END: {tag}' + END)
            return result
        return wrapper
    return _timer


