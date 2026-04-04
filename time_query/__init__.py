import time_query.runtime as rt

from pathlib import Path
from mcdreforged.api.all import PluginServerInterface
from time_query.config import DefaultConfig, SupportedLanguages, resource_extractor, tr
from time_query.command import command_register


def load_i18n(s: PluginServerInterface, lang_dir: Path):
    for i in SupportedLanguages:
        _f = f"{i}.yml"
        file = Path("lang") / _f
        file_target = lang_dir / _f
        if not file_target.exists():
            resource_extractor(s, file, file_target)
            break
        lang_map = s.load_config_simple(str(file), echo_in_console=False)
        if isinstance(lang_map, dict):
            s.logger.info(f"Registering i18n for plugin time_query: '{i}'")
            s.register_translation(i, lang_map)


def on_load(s: PluginServerInterface, old):
    first_load: bool = False
    config_fp = Path(s.get_data_folder()) / "config.yml"
    if not config_fp.exists():
        first_load = True
    rt.config = s.load_config_simple("config.yml", target_class=DefaultConfig)  # ty: ignore[invalid-assignment]
    config_dir = s.get_data_folder()
    lang_dir = Path(config_dir) / "lang"
    if not lang_dir.is_dir():
        lang_dir.mkdir(exist_ok=True)
    if not rt.config.i18n_lock:
        load_i18n(s, lang_dir)
    else:
        if first_load:
            s.logger.info(tr(s, "i18n_modify_tip"))
    s.logger.info(tr(s, "i18n_finish"))
    command_register(s)
    s.logger.info(tr(s, "plugin_loaded"))


def on_server_startup(s: PluginServerInterface):
    pass
