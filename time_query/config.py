from pathlib import Path
from packaging import version
from typing import Literal
from mcdreforged.api.all import (
    Serializable,
    PluginServerInterface,
    RTextMCDRTranslation,
)

MCVersionMode = Literal["26.x", "1.x"]
SupportedLanguages: list[str] = ["zh_cn", "en_us"]


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
    return version.parse(ver) >= version.parse(target)


def check_server_version(s: PluginServerInterface) -> MCVersionMode:
    version = s.get_server_information().version
    if version:
        if is_version_ge(version, "26"):
            return "26.x"
    else:
        s.logger.warning(tr(s, "return_default_ver_mode"))
    return "1.x"


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
