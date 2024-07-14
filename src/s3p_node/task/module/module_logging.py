import functools
import logging


def log(module):
    @functools.wraps(module)
    def wrapper(*args, **kwargs):
        print(args)
        logger = logging.getLogger(module.__class__.__name__)
        _name = ''
        if len(args) == 3 and isinstance(args[3], str):
            _name = args[2]

        logger.info(f"module '{_name}' start")
        result = module(*args, **kwargs)
        logger.info(f"module '{_name}' done")
        return result

    return wrapper
