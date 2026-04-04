import locale
import re

import arrow
from mcdreforged import PluginServerInterface
from tzlocal import get_localzone

import time_query.runtime as rt
from time_query.config import MCVersionMode, tr_to_str


class RealTimeQueryer:
    def __init__(self):
        self.s = rt.psi

    @classmethod
    def get_locale(cls) -> str | None:
        lang, enc = locale.getlocale()
        return lang

    def get_locale_supported(self, lang: str | None) -> str:
        if rt.config.force_language is not None:
            if rt.config.force_language != "":
                return rt.config.force_language
        mcdr_lang = self.s.get_mcdr_language()
        if lang:
            if "zh_cn" in lang.lower():
                return "zh_cn"
            elif "zh_tw" in lang.lower():
                return "zh_tw"
            elif "zh" in mcdr_lang:
                return mcdr_lang
        return "en_us"

    @classmethod
    def get_time_zone(cls) -> str:
        if rt.config.force_timezone is not None:
            if rt.config.force_timezone != "":
                return rt.config.force_timezone
        return get_localzone().key

    def get_time(self, timezone: str) -> arrow.Arrow:
        return arrow.now(timezone)

    def get_time_readable(
        self, lang: str, timezone: str, time_obj: arrow.Arrow | None = None
    ) -> str:
        if not time_obj:
            time_obj = self.get_time(timezone)
        return time_obj.to(timezone).format(
            tr_to_str(self.s, "prefix.time_format"), lang
        )

    def get_date_readable(
        self, lang: str, timezone: str, time_obj: arrow.Arrow | None = None
    ) -> str:
        if not time_obj:
            time_obj = self.get_time(timezone)
        return time_obj.to(timezone).format(
            tr_to_str(self.s, "prefix.date_format"), lang
        )

    def get_complete_time(self, lang: str, timezone: str) -> str:
        time_readable = self.get_time_readable(lang, timezone)
        date_readable = self.get_date_readable(lang, timezone)
        return date_readable + " " + time_readable


class InGameTimeQueryer:
    def __init__(self, s: PluginServerInterface = rt.psi):
        self.s = s

    def _parser(
        self, command_reply: str, mode: MCVersionMode = rt.mc_version
    ) -> int | None:
        match mode:
            case MCVersionMode.V26_x:
                pattern = r"^Timeline [a-z0-9_]+:[a-z0-9_]+ is at (\d+) tick\(s\)$"
                if match_obj := re.match(pattern, command_reply):
                    return int(match_obj.group(1))
            case MCVersionMode.V26_x:
                pattern = r"^The\s+time\s+is\s+(\d+)$"
                if match_obj := re.match(pattern, command_reply):
                    return int(match_obj.group(1))

    def get_command(self, mode: MCVersionMode = rt.mc_version):
        match mode:
            case MCVersionMode.V26_x:
                return "time query day"
            case MCVersionMode.V1_x:
                return "time query daytime"

    async def get_time_raw(self, mode: MCVersionMode = rt.mc_version) -> int:
        if rt.rcon_api:
            rcon_api = rt.rcon_api
            command_reply = await rcon_api.rcon_get_result(
                self.s, self.get_command(mode)
            )
        else:
            command_reply = self.s.rcon_query(self.get_command(mode))
        if not command_reply:
            self.s.logger.error("Failed to get time from rcon.")
            raise RuntimeError("Failed to get time from rcon.")
        else:
            result = self._parser(command_reply, mode)
            if result:
                return result
            raise TypeError(f"Failed to parse command reply: {result}")

    async def get_time(self, mode: MCVersionMode = rt.mc_version) -> str:
        _time = (await self.get_time_raw(mode) + 6000) % 24000
        _hour = int(_time / 1000)
        _minute = int((_time % 1000) / 1000 * 60)
        result = tr_to_str(self.s, "prefix.game_time_format")
        result = result.replace("h", str(_hour)).replace("m", str(_minute))
        return result
