# coding=utf-8
"""
This script used for running UkrnetNewsBot
"""

import time
import asyncio

from ukrnet_news.bot import UkrnetNewsBot, refresher
from ukrnet_news.config import TELEGRAM


if __name__ == "__main__":
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
