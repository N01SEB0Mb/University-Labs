# coding=utf-8

import asyncio
import logging

from .bot import UkrnetNewsBot

from ukrnet_news.config import CONFIG
from ukrnet_news.utils import async_exception_handler


@async_exception_handler
async def refresher(bot: UkrnetNewsBot, interval: int = CONFIG["news"]["refresh_interval"]) -> None:
    """
    This function refreshes news in infinite loop with specified interval

    Args:
        bot (UkrnetNewsBot): News bot
        interval (int): News refreshing interval (in seconds). Defaults by configured value
    """

    while True:

        # Refresh news stream
        logging.info("Time to refresh news")
        await bot.refresh_news()

        # Wait for specified interval
        logging.info(f"Sleeping until next refresh ({interval} seconds)")
        await asyncio.sleep(interval)
