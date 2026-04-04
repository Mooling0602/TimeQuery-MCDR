from mcdreforged.api.all import ServerInterface

try:
    import moolings_rcon_api as rcon_api
except (ModuleNotFoundError, ImportError):
    rcon_api = None  # ty: ignore[invalid-assignment]

from time_query.config import DefaultConfig, MCVersionMode

config: DefaultConfig = DefaultConfig()
psi = ServerInterface.psi()
mc_version: MCVersionMode = MCVersionMode.V1_x
