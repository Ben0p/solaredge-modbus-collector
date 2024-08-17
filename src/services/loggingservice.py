import logging



'''
Module to intialize logging
'''



def init_logging(logging_level):

    # Set logging level
    match logging_level.lower().strip():
        case 'debug':
            logging_level = logging.DEBUG
        case 'info':
            logging_level = logging.INFO
        case 'warning':
            logging_level = logging.WARNING
        case 'error':
            logging_level = logging.ERROR
        case 'critical':
            logging_level = logging.CRITICAL
        case 'default':
            logging_level = logging.INFO
        case _:
            logging_level = logging.INFO
            
    # Set up logging
    logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    logger.info(f'Logging level set to "{logging.getLevelName(logger.level)}"')

    return logger