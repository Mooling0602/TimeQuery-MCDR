from pathlib import Path
import time_query.runtime as rt

from mcdreforged.api.all import (
    PluginServerInterface,
    SimpleCommandBuilder,
    CommandSource,
    CommandContext,
)
from time_query.config import PluginCommand, tr
from time_query.query import RealTimeQueryer

default_command_set = PluginCommand()
builder = SimpleCommandBuilder()
queryer = RealTimeQueryer()
_cmd_pfx: str = default_command_set.pfx
_cmd_root_node: str = default_command_set.root_node
_cmd_control_config_reset: bool = False


def command_register(s: PluginServerInterface):
    global _cmd_root_node
    if rt.config.command.enable_namespace:
        _cmd_root_node = s.get_self_metadata().id + ":" + _cmd_root_node
    builder.register(s)


@builder.command(f"{_cmd_pfx}{_cmd_root_node}")
async def on_main_command(src: CommandSource):
    src.reply("Usage: !!time [real]")


def _require_console(src: CommandSource) -> bool:
    s = src.get_server().psi()
    if not src.is_console:
        src.reply(tr(s, "require_console_permission"))
        return True
    return False


@builder.command(f"{_cmd_pfx}{_cmd_root_node} real")
async def on_get_real_time(src: CommandSource):
    lang = queryer.get_locale_supported(queryer.get_locale())
    timezone = queryer.get_time_zone()
    src.reply(queryer.get_complete_time(lang, timezone))


@builder.command(f"{_cmd_pfx}time_query:debug config")
async def on_debug_config(src: CommandSource):
    src.reply("Plugin configuration:")
    src.reply(str(rt.config))


@builder.command(f"{_cmd_pfx}time_query:config reset")
@builder.command(f"{_cmd_pfx}time_query:config reset --confirm")
async def on_reset_config(src: CommandSource, ctx: CommandContext):
    s = src.get_server().psi()
    global _cmd_control_config_reset
    if _require_console(src):
        return
    if "--confirm" in ctx.command or _cmd_control_config_reset is True:
        config_file = Path(s.get_data_folder()) / "config.yml"
        config_file.rename("config.yml.bak")
        _cmd_control_config_reset = False
        src.reply("config_reset_success")
    else:
        src.reply("please_confirm_option")
        _cmd_control_config_reset = True


@builder.command(f"{_cmd_pfx}time_query:helper update_i18n")
@builder.command(f"{_cmd_pfx}time_query:helper update_i18n --reload")
def on_update_i18n(src: CommandSource, ctx: CommandContext):
    s = src.get_server().psi()
    if _require_console(src):
        return
    config_dir = Path(s.get_data_folder()) / "lang"
    do_update: bool = False
    if config_dir.exists() and config_dir.is_dir():
        for i in config_dir.iterdir():
            if not str(i).endswith(".bak"):
                if not do_update:
                    do_update = True
                i.rename(f"{i}.bak")
        if "--reload" in ctx.command:
            s.reload_plugin(s.get_self_metadata().id)
            return
    if do_update:
        src.reply("Please reload this plugin to take effort.")
    else:
        src.reply("Updated i18n, please reload this plugin first.")
        src.reply(
            f"Old *.bak files will block update, please sync your modifications first, then execute command `{_cmd_pfx}time_query:helper rmcache_i18n` in console to unblock."
        )


@builder.command(f"{_cmd_pfx}time_query:helper rmcache_i18n")
@builder.command(f"{_cmd_pfx}time_query:helper rmcache_i18n --confirm")
@builder.command(f"{_cmd_pfx}time_query:helper rmcache_i18n --update")
def on_rmcache_i18n(src: CommandSource, ctx: CommandContext):
    s = src.get_server().psi()
    src.reply(
        f"Remove old *.bak files in '{Path(s.get_data_folder()) / 'lang'}' manually, please."
    )
    raise NotImplementedError()
