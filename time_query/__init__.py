import arrow

from typing import Optional
from mcdreforged.api.all import *

prefixReal_zh = "[现实时间]"
prefixReal_en = "[Real Time]"
prefixGame_zh = "[游戏内时间]"
prefixGame_en = "[Game Time]"

psi = ServerInterface.psi()

default_config = {
    "locale": ""
}

config = psi.load_config_simple("config.json", default_config)
locale = None

def build_command(maincmd: Optional[str] = "time"):
    psi.register_command(
        Literal(f"!!{maincmd}")
        .runs(
            lambda src: src.reply(getTime())
        )
        .then(
            Literal("real")
            .runs(
                lambda src: src.reply(getRealTime())
            )
        )
        .then(
            Literal("game")
            .runs(
                lambda src: src.reply(getGameTime())
            )
        )
    )

def on_load(server: PluginServerInterface, old):
    global config, locale
    server.logger.info("Loading TimeQuery.")
    locale = config.get("locale", None)
    build_command()
    # Add prefix as an aliase command to avoid conflict. 
    build_command("time_query:time")
    server.logger.info("Commands registered.")

def getTime():
    if locale == "":
        return getRealTime() + "\n" + getGameTime()
    elif locale == "zh":
        return prefixReal_zh + getRealTime() + "\n" + prefixGame_zh + getGameTime()
    elif locale == "en":
        return prefixReal_en + getRealTime() + "\n" + prefixGame_en + getGameTime()
    elif locale is None:
        return "Error: config option lost."
    else:
        return "Error: not support this locale"

def getRealTime():
    global locale
    if locale == "":
        return arrow.now().format("YYYY-MM-DD" + arrow.now().format("d") + "HH:mm:ss") + " " + arrow.now().tzname()
    elif locale == "zh":
        if arrow.now().tzname() == "CST":
            return arrow.now().format("YYYY年MM月DD日 dddd HH时mm分ss秒", locale='zh') + " " + "中国标准时间"
        else:
            return arrow.now().format("YYYY年MM月DD日 dddd HH时mm分ss秒", locale='zh') + " " + arrow.now().tzname()
    elif locale == "en":
        return arrow.now().format("MMMM D, YYYY dddd HH:mm:ss") + " " + arrow.now().tzname()
    elif locale is None:
        return "Error: config option lost."
    else:
        return "Error: not support this locale."

def getGameTime():
    return "null"
