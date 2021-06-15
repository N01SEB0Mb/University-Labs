# coding=utf-8

import asyncio

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
        bot.refresh_news()

        # Wait for specified interval
        await asyncio.sleep(interval)
