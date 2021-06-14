# created by noisebomb

# coding=utf-8

import json
import source
import asyncio
from copy import deepcopy
from requests.exceptions import RequestException
from time import sleep, strftime
from aiogram import Bot
from aiogram.utils.markdown import hbold, hlink
from aiogram.utils.exceptions import TelegramAPIError


async def checker():
    global new
    p = source.Parser(config)

    while True:
        with open("last.news", "rt") as last_file:
            try:
                last = set(map(int, last_file.read().split(" ")))
            except ValueError:
                last = set()

        last_update = p.get_last()
        news = deepcopy(last_update - last)

        with open("last.news", "wt") as last_file:
            last_file.write(" ".join(map(lambda x: str(x["Id"]), last_update)))

        summary = len(news)
        count = 0

        for new in news:
            try:
                info = p.get_info(new)
            except (RequestException, BaseException) as err:
                print(time() + str(err) + ": " + str(new))
                if config["logging"]:
                    with open("exception.log", "a") as logFile:
                        logFile.write(time() + str(error) + ": " + str(new) + "\n")
        for new in news:
            try:
                info = p.get_info(new)
            except BaseException as err:
                print(time() + str(err) + ": " + str(new))
                if config["logging"]:
                    with open("exception.log", "a") as logFile:
                        logFile.write(time() + str(err) + ": " + str(new) + "\n")
            else:
                if info:
                    title, description, image = info
                    msg = f'{hbold(title)}\n\n{description}{hlink("Подробнее", new["Url"])}'
                    try:
                        if image:
                            await bot.send_photo(tg_info["channelId"], image, caption=msg, parse_mode="HTML")
                        else:
                            await bot.send_message(tg_info["channelId"], msg, parse_mode="HTML")
                    except TelegramAPIError as error:
                        print(time() + str(error) + ": " + str(new))
                        if config["logging"]:
                            with open("exception.log", "a") as logfile:
                                logfile.write(time() + str(error) + ": " + str(new) + "\n")
                    else:
                        count += 1
                elif info is None:
                    print(time() + "no info: " + str(new))
                    if config["logging"]:
                        with open("exception.log", "a") as logfile:
                            logfile.write(time() + "no info: " + str(new) + "\n")
                else:
                    print(time() + "request error: " + str(new))
                    if config["logging"]:
                        with open("exception.log", "a") as logfile:
                            logfile.write(time() + "request error: " + str(new) + '\n')

        print(time() + "checking finished, posted {0}/{1}".format(count, summary))
        if config["logging"]:
            with open("exception.log", "a") as logfile:
                logfile.write(time() + "checking finished, posted {0}/{1}\n".format(count, summary))
                if image:
                    await bot.send_photo(tg_info["channelId"], image, caption=msg, parse_mode="HTML")
                else:
                    await bot.send_message(tg_info["channelId"], msg, parse_mode="HTML")

        print(time() + "checking finished")
        if config["logging"]:
            with open("exception.log", "a") as logfile:
                logfile.write(time() + "checking finished\n")

        await asyncio.sleep(config["sleep"])


if __name__ == "__main__":
    with open("config.json", "rb") as config_file:
        config = json.load(config_file)

    with open("tg.json", "rb") as tg_file:
        tg_info = json.load(tg_file)

    time = lambda: strftime("[%H:%M:%S %d.%m.%Y ") + "UTC" + strftime("%z")[:3] + ":" + strftime("%z] ")[3:]
    new = None

    while True:
        bot = Bot(tg_info["botToken"])
        aio_loop = asyncio.get_event_loop()

        try:
            aio_loop.run_until_complete(checker())
        except KeyboardInterrupt:
            pass
        except BaseException as err:
            print(time() + str(err) + ": " + str(new))
            if config["logging"]:
                with open("exception.log", "a") as log_file:
                    log_file.write(time() + str(err) + ": " + str(new) + "\n")
        finally:
            aio_loop.run_until_complete(bot.close())
            print(time() + "loop finished")
            if config["logging"]:
                with open("exception.log", "a") as log_file:
                    log_file.write(time() + "loop finished\n")

            sleep(config["retrySleep"])
