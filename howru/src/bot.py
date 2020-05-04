from handlers import error_callback
from log.logger import logger
from telegram.ext import Updater

from config import bot_config
from handlers.start_handler import start_handler


def main():
    logger.info("Started HOW-R-U psychologist")
    # Initialize bot
    updater = Updater(token=bot_config.TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    handlers = [start_handler]
    # Add handlers to dispatcher
    for handler in handlers:
        dispatcher.add_handler(handler)
    # Add error callback
    dispatcher.add_error_handler(error_callback)
    # Start bot service
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
