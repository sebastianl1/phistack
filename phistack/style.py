import json
import shutil

from . import paths, fractal
from .lang import t

BANNER_SIZES = ("small", "medium", "large")
_banner_cache = {}


def render_banner(size="small"):
    if size not in BANNER_SIZES:
        size = "small"
    if size not in _banner_cache:
        _banner_cache[size] = fractal.build(size)
    return _banner_cache[size]


def set_banner(size):
    if size not in BANNER_SIZES:
        return False
    config = _load_config()
    config["banner"] = size
    _save_config(config)
    return True


def set_prompt(style):
    config = _load_config()
    config["prompt"] = style
    _save_config(config)
    return True


def set_prompt_username(username):
    config = _load_config()
    config["prompt_username"] = username
    _save_config(config)
    return True


def _load_config():
    cfg = {}
    if paths.CONFIG_FILE.exists():
        try:
            with open(paths.CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, json.JSONDecodeError):
            cfg = {}
    return cfg


def _save_config(config):
    paths.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(paths.CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def apply_termux_theme():
    termux_dir = paths.HOME / ".termux"
    if termux_dir.exists():
        shutil.rmtree(termux_dir)
    termux_dir.mkdir(parents=True, exist_ok=True)

    props_src = paths.STYLE_DIR / "termux.properties"
    colors_src = paths.STYLE_DIR / "colors.properties"
    if props_src.exists():
        shutil.copy(props_src, termux_dir / "termux.properties")
    if colors_src.exists():
        shutil.copy(colors_src, termux_dir / "colors.properties")
    return True


def apply_fish_prompt(style="phistack"):
    fish_func_dir = paths.HOME / ".config" / "fish" / "functions"
    fish_func_dir.mkdir(parents=True, exist_ok=True)
    src = paths.STYLE_DIR / "fish_prompt.fish"
    dest = fish_func_dir / "fish_prompt.fish"
    if style == "default":
        src = paths.STYLE_DIR / "fish_prompt.default"
    if src.exists():
        shutil.copy(src, dest)
    return True
