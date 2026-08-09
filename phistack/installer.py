import hashlib
import os
import shutil
import subprocess
import sys

from . import paths, state
from .lang import t

TERMUX_ENV = {
    "HOME": str(paths.HOME),
    "PREFIX": str(paths.PREFIX),
    "BIN": str(paths.BIN),
    "OPT": str(paths.OPT),
    "ETC": str(paths.ETC),
    "SHARE": str(paths.SHARE),
    "PHISTACK": str(paths.REPO_ROOT),
}


def expand(text):
    for key, value in TERMUX_ENV.items():
        text = text.replace(f"${key}", value).replace("${" + key + "}", value)
    return text


def run(cmd, cwd=None):
    proc = subprocess.run(
        expand(cmd),
        shell=True,
        cwd=expand(cwd) if cwd else None,
        text=True,
    )
    return proc.returncode == 0


def run_step(step):
    method = step.get("method")
    if method == "vendor":
        name = step["name"]
        src = paths.REPO_ROOT / "lab" / "tools" / name
        dest = paths.OPT / name
        if not src.exists():
            return False
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src, dest)
        return True
    if method == "pkg":
        packages = " ".join(step["packages"])
        return run(f"pkg install -y {packages}")
    if method == "git":
        name = step["name"]
        url = step["url"]
        dest = _dest_path(step.get("dest", "opt"), name)
        if not os.path.exists(dest):
            paths.OPT.mkdir(parents=True, exist_ok=True)
            return run(f"git clone --depth 1 {url} {dest}")
        return True
    if method == "pip":
        packages = " ".join(step["packages"])
        return run(f"{sys.executable} -m pip install --quiet {packages}")
    if method == "run":
        cwd = step.get("cwd")
        return run(step["cmd"], cwd=cwd)
    if method == "download":
        url = step["url"]
        path = expand(step["path"])
        expected = step.get("sha256")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not run(f"wget --quiet -O {path} {url}"):
            return False
        if expected and not _sha256(path, expected):
            return False
        os.chmod(path, 0o755)
        return True
    if method == "launcher":
        name = step["name"]
        script = expand(step["script"])
        script = _fix_shebang(script)
        path = paths.BIN / name
        paths.BIN.mkdir(parents=True, exist_ok=True)
        path.write_text(script, encoding="utf-8")
        path.chmod(0o755)
        return True
    return False


def _fix_shebang(script):
    lines = script.splitlines()
    if lines and lines[0].startswith("#!"):
        interpreter = lines[0][2:].strip()
        if interpreter in ("/bin/bash", "/bin/sh", "bash", "sh"):
            lines[0] = f"#!{paths.PREFIX}/bin/bash"
    return "\n".join(lines) + "\n"


def _dest_path(base, name):
    base = base.strip()
    if base.startswith("$"):
        return expand(os.path.join(base, name))
    key = base.upper()
    if key in TERMUX_ENV:
        return expand(os.path.join("$" + key, name))
    return expand(os.path.join(base, name))


def _sha256(path, expected):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest() == expected


def verify_tool(tool):
    verify = tool.get("verify", {})
    if "cmd" in verify:
        result = subprocess.run(
            expand(verify["cmd"]),
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    if "exists" in verify:
        return os.path.exists(expand(verify["exists"]))
    if "bin" in verify:
        return shutil.which(expand(verify["bin"])) is not None
    return False


def installed_by_verify(tool):
    return bool(verify_tool(tool))


def install_tool(tool):
    tool_id = tool["id"]
    if state.is_installed(tool_id) or installed_by_verify(tool):
        return True, "already"
    for step in tool.get("install", []):
        if not run_step(step):
            return False, "error"
    state.mark_installed(tool_id)
    return True, "ok"


def remove_tool(tool):
    tool_id = tool["id"]
    ok = True
    for step in tool.get("remove", []):
        if not run_step(step):
            ok = False
    state.mark_removed(tool_id)
    return ok


def need_dependencies():
    missing = []
    for mod in ("InquirerPy", "rich"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing


def ensure_dependencies():
    missing = need_dependencies()
    if missing:
        run(f"{sys.executable} -m pip install --quiet {' '.join(missing)}")
    return need_dependencies()
