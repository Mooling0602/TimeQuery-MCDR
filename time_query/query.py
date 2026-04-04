from time_query.config import tr_to_str
import locale
import arrow
import time_query.runtime as rt

from tzlocal import get_localzone


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
