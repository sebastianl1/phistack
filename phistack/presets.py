import os
import shutil
import subprocess
import time

from . import paths
from .lang import t

TERM_DIR = paths.REPO_ROOT / "lab" / "termux"
SHELL_DIR = paths.REPO_ROOT / "lab" / "shell"
IDE_DIR = paths.REPO_ROOT / "lab" / "ide"
BANNERS_DIR = TERM_DIR / "banners"
PROMPTS_DIR = SHELL_DIR / "prompts"
INSTALLED_BANNERS = paths.OPT / "phistack" / "banners"

ETC_MOTD = paths.ETC / "motd.sh"
ETC_BASHRC = paths.ETC / "bash.bashrc"
TERMUX_HOME = paths.HOME / ".termux"
FISH_FUNC = paths.HOME / ".config" / "fish" / "functions" / "fish_prompt.fish"
FISH_CONFIG = paths.HOME / ".config" / "fish" / "config.fish"
NVIM_CONFIG = paths.HOME / ".config" / "nvim"


def _list_dirs(base):
    if not base.exists():
        return []
    return sorted(d.name for d in base.iterdir() if d.is_dir())


def term_presets():
    return [d for d in _list_dirs(TERM_DIR) if d != "banners"]


def shell_presets():
    return [d for d in _list_dirs(SHELL_DIR) if d != "prompts"]


def ide_presets():
    return _list_dirs(IDE_DIR)


def banner_styles():
    styles = [p.stem for p in BANNERS_DIR.glob("*.txt")]
    if (BANNERS_DIR / "phi.sh").exists():
        styles.append("phi")
    return sorted(styles)


def prompt_styles():
    return [p.stem for p in PROMPTS_DIR.glob("*.fish")]


def apply_term_preset(name):
    src = TERM_DIR / name
    if not src.is_dir():
        raise FileNotFoundError(name)
    TERMUX_HOME.mkdir(parents=True, exist_ok=True)
    copied = []
    for f in ("termux.properties", "colors.properties", "font.ttf"):
        if (src / f).exists():
            shutil.copy2(src / f, TERMUX_HOME / f)
            copied.append(f)
    try:
        subprocess.run(["termux-reload-settings"], capture_output=True)
    except (FileNotFoundError, OSError):
        pass
    return copied


def set_banner(style):
    if style == "phi":
        src = BANNERS_DIR / "phi.sh"
        if src.exists():
            shutil.copy2(src, ETC_MOTD)
            os.chmod(ETC_MOTD, 0o755)
            return True
        return False
    data = BANNERS_DIR / f"{style}.txt"
    if not data.exists():
        return False
    INSTALLED_BANNERS.mkdir(parents=True, exist_ok=True)
    dest_data = INSTALLED_BANNERS / f"{style}.txt"
    shutil.copy2(data, dest_data)
    template = BANNERS_DIR / "motd-generic.sh"
    content = template.read_text(encoding="utf-8").replace("__BANNER__", str(dest_data))
    ETC_MOTD.write_text(content, encoding="utf-8")
    os.chmod(ETC_MOTD, 0o755)
    return True


def set_prompt(style):
    src = PROMPTS_DIR / f"{style}.fish"
    if not src.exists():
        return False
    FISH_FUNC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, FISH_FUNC)
    return True


def set_shell(style):
    src = SHELL_DIR / style
    if not src.is_dir():
        raise FileNotFoundError(style)
    changed = []
    cfg = src / "config.fish"
    if cfg.exists():
        FISH_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cfg, FISH_CONFIG)
        changed.append("config.fish")
    prompt = src / "fish_prompt.fish"
    if prompt.exists():
        FISH_FUNC.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(prompt, FISH_FUNC)
        changed.append("fish_prompt.fish")
    bashrc = src / "bash.bashrc"
    if bashrc.exists():
        shutil.copy2(bashrc, ETC_BASHRC)
        changed.append("bash.bashrc")
    return changed


def save_term(name):
    dest = TERM_DIR / name
    dest.mkdir(parents=True, exist_ok=True)
    copied = []
    for f in ("termux.properties", "colors.properties", "font.ttf"):
        src = TERMUX_HOME / f
        if src.exists():
            shutil.copy2(src, dest / f)
            copied.append(f)
    return copied


def save_shell(name):
    dest = SHELL_DIR / name
    dest.mkdir(parents=True, exist_ok=True)
    copied = []
    pairs = [
        (FISH_CONFIG, dest / "config.fish"),
        (FISH_FUNC, dest / "fish_prompt.fish"),
        (ETC_BASHRC, dest / "bash.bashrc"),
    ]
    for src, dst in pairs:
        if src.exists():
            shutil.copy2(src, dst)
            copied.append(dst.name)
    return copied


def ide_install(name):
    src = IDE_DIR / name
    if not src.is_dir():
        raise FileNotFoundError(name)
    if NVIM_CONFIG.exists():
        backup = IDE_DIR / f"backup-{int(time.time())}"
        shutil.copytree(NVIM_CONFIG, backup)
    shutil.rmtree(NVIM_CONFIG, ignore_errors=True)
    shutil.copytree(src, NVIM_CONFIG)
    return True


def ide_backup():
    if not NVIM_CONFIG.exists():
        return None
    backup = IDE_DIR / f"backup-{int(time.time())}"
    shutil.copytree(NVIM_CONFIG, backup)
    return backup


def ide_edit():
    editor = os.environ.get("EDITOR", "nvim")
    if NVIM_CONFIG.exists():
        subprocess.run([editor, str(NVIM_CONFIG)])
