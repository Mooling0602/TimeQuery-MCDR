import re
from enum import Enum
from pathlib import Path
from typing import Literal

from mcdreforged.api.all import (
    PluginServerInterface,
    RTextMCDRTranslation,
    Serializable,
)
from packaging import version
from packaging.version import InvalidVersion

SupportedLanguages: list[str] = ["zh_cn", "en_us"]


class MCVersionMode(Enum):
    V1_x = "1.x"
    V26_x = "26.x"


class RconSettings(Serializable):
    force_require: bool = False
    api: Literal["mcdr", "moolings_rcon_api"] = "moolings_rcon_api"


class PluginCommand(Serializable):
    pfx: str = "!!"
    root_node = "time"
    enable_namespace: bool = False


class DefaultConfig(Serializable):
    force_language: str = ""
    force_timezone: str = ""
    i18n_lock: bool = True
    rcon: RconSettings = RconSettings()
    command: PluginCommand = PluginCommand()


def is_version_ge(ver: str, target: str) -> bool:
    def _clean(v: str) -> str | None:
        match = re.search(r"(\d+(\.\d+)*)", v)
        return match.group(1) if match else None

    def _get_result(v: str) -> bool:
        return version.parse(v) >= version.parse(target)

    try:
        return _get_result(ver)
    except InvalidVersion:
        _ver = _clean(ver)
        if _ver is not None:
            return _get_result(_ver)
        else:
            raise


def check_server_version(s: PluginServerInterface) -> MCVersionMode:
    version = s.get_server_information().version
    if version:
        if is_version_ge(version, "26"):
            return MCVersionMode.V26_x
    else:
        s.logger.warning(tr(s, "return_default_ver_mode"))
    return MCVersionMode.V1_x


def resource_extractor(
    s: PluginServerInterface, file_path: Path | str, target_path: Path | str
):
    try:
        file_path = str(file_path)
        target_path = str(target_path)
        with s.open_bundled_file(file_path) as fh:
            with open(target_path, "wb") as f:
                f.write(fh.read())
                s.logger.debug(f"Extracted <PluginFile>/{file_path} to {target_path}")
    except Exception as e:
        s.logger.critical(f"Failed to extract plugin resource '{file_path}': {e}")


def tr(
    server: PluginServerInterface, tr_key: str, return_str: bool = False, *args
) -> str | RTextMCDRTranslation:
    plg_id = server.get_self_metadata().id
    if tr_key.startswith(f"{plg_id}"):
        translation = server.rtr(f"{tr_key}")
    else:
        if tr_key.startswith("#"):
            translation = server.rtr(tr_key.replace("#", ""), *args)
        else:
            translation = server.rtr(f"{plg_id}.{tr_key}", *args)
    if return_str:
        tr_to_str: str = str(translation)
        return tr_to_str
    else:
        return translation


def tr_to_str(server: PluginServerInterface, tr_key: str, *args) -> str:
    return str(tr(server, tr_key, True, *args))
