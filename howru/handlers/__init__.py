from log.logger import logger

def error_callback(update, context):
    logger.error(f'Error {context.error} while performing update {update}')