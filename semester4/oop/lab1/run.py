# coding=utf-8
"""
This script used for running UkrnetNewsBot
"""

import time
import asyncio
import logging
from pathlib import Path

from ukrnet_news.bot import UkrnetNewsBot, refresher
from ukrnet_news.config import CONFIG, TELEGRAM


if __name__ == "__main__":

    # Define log file handler path + create directories
    file_handler_path = Path().resolve() / "logs" / "bot.log"
    file_handler_path.parent.mkdir(parents=True, exist_ok=True)

    # Setup basic logging config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),  # Add stream handler (log into console)
            logging.FileHandler(file_handler_path)  # Add file handler (log into file)
        ]
    )

    # Run infinite loop

    while True:
        # Create bot instance
        news_bot = UkrnetNewsBot(TELEGRAM["bot"]["token"])

        # Run asyncronyous loop
        async_loop = asyncio.get_event_loop()
        async_loop.run_until_complete(refresher(news_bot))

        # Close bot after 'checker' ending (some exception occurred)
        async_loop.run_until_complete(news_bot.close())

        # Sleep for configured number of seconds
        time.sleep(10)
