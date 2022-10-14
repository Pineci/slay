from pathlib import Path

### PATHS
PROJECT_DIR = Path.home().joinpath("Documents", "Projects", "slay") #Path("~/Desktop/Projects/slay").expanduser()
ALL_ASSET_DIR = PROJECT_DIR.joinpath("assets")
TILE_ASSET_DIR = ALL_ASSET_DIR.joinpath("tileassets")
TEXTURE_ASSET_DIR = ALL_ASSET_DIR.joinpath("textures")
DEFAULT_TEXTURE_SCALE = 13