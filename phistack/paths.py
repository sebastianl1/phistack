import os
import pathlib

HOME = pathlib.Path.home()
PREFIX = pathlib.Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"))

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG_FILE = REPO_ROOT / "catalog" / "tools.json"
STYLE_DIR = REPO_ROOT / "style"

CONFIG_DIR = HOME / ".phistack"
CONFIG_FILE = CONFIG_DIR / "config.json"
STATE_FILE = CONFIG_DIR / "state.json"
CACHE_FILE = CONFIG_DIR / "cache.json"

BIN = PREFIX / "bin"
OPT = PREFIX / "opt"
ETC = PREFIX / "etc"
SHARE = PREFIX / "share"
