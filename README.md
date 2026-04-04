# TimeQuery-MCDR
A MCDR(full name "MCDReforged") plugin use to query the time in real and game.

README will written only by zh_CN, you can translate it with AI tools.

> Since Minecraft 26.1, the usage of `/time` has changed, and newer version of this plugin will support it.

# 用途
查询现实和游戏内的时间，以24小时制显示。

> 自Minecraft 26.1以后，`/time`的用法发生了改变，插件的新版本将支持这一改变。

# 配置
插件主配置在"config/time_query/config.yml"。

如果需要修改插件翻译，请关闭`i18n_lock`项。

# 用法
`!!time` - 查询现实和游戏内的时间，并分别显示

`!!time real` - 仅查询现实的时间，显示年月日、星期几、具体时间（精确到秒）

`!!time game` - 仅查询游戏内的时间，对应现实24小时制精确到分（需要Rcon支持，若无法使用Rcon环境且游戏版本在26.1以前，可以尝试插件仓库中的Daytime插件）

# 指令冲突问题
同时注册了`!!time_query:time`等效于`!!time`，若发生冲突可使用这个带上了前缀的指令

你也可以在插件配置中，修改指令别名，或使用命名空间前缀作为默认值。

