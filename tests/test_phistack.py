import json
import subprocess
import sys

import pytest

from phistack import catalog, installer, paths, state, fractal


def test_fractal_banner_no_name():
    banner = fractal.build("small")
    assert "PHISTACK" not in banner
    assert "\x1b[" in banner
    assert "▀" in banner


def test_fractal_full_set_has_interior():
    cols, rows = 120, 60
    px = fractal.fractal_pixels(cols, rows, 80)
    interior = sum(1 for row in px for c in row if c == fractal.INTERIOR)
    ratio = interior / (cols * rows)
    assert 0.05 < ratio < 0.6


def test_catalog_loads_and_validates():
    errs = catalog.validate()
    assert errs == []


def test_catalog_min_tools():
    assert len(catalog.list_tools()) >= 70


def test_catalog_has_categories():
    for cat in ["osint", "scan", "web", "exploit", "crack", "phishing", "wireless", "forense", "utils"]:
        assert cat in catalog.category_ids()


def test_catalog_tool_fields():
    tool = catalog.get_tool("nmap")
    assert tool is not None
    assert tool["status"] == "active"
    assert tool["desc_es"] and tool["desc_en"]
    assert tool["install"]


def test_search_phone():
    results = catalog.search_tools("phone")
    ids = {r["id"] for r in results}
    assert "phoneinfoga" in ids


def test_obsolete_have_replacement():
    for tool in catalog.list_tools(status="obsolete"):
        assert tool.get("replacement"), f"{tool['id']} obsoleta sin replacement"


def test_expand_prefix():
    assert "$PREFIX" not in installer.expand("echo $PREFIX")
    assert installer.expand("x $BIN y") == f"x {paths.BIN} y"


def test_dest_path_resolves_opt():
    dest = installer._dest_path("opt", "demo")
    assert dest == f"{paths.OPT}/demo"


def test_dest_path_dollar():
    dest = installer._dest_path("$OPT/sub", "demo")
    assert dest == f"{paths.OPT}/sub/demo"


def test_fix_shebang():
    fixed = installer._fix_shebang("#!/bin/bash\necho hi")
    assert fixed.startswith(f"#!{paths.PREFIX}/bin/bash")


def test_state_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(paths, "STATE_FILE", tmp_path / "state.json")
    state.mark_installed("demo")
    assert state.is_installed("demo")
    state.mark_removed("demo")
    assert not state.is_installed("demo")


def test_lang_bilingual(tmp_path, monkeypatch):
    from phistack import lang

    monkeypatch.setattr(paths, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(paths, "CONFIG_FILE", tmp_path / "config.json")
    lang.set_lang("en")
    assert lang.load_lang() == "en"
    assert lang.t("tool_name") == "Tool"
    assert lang.t("install_ok", tool="Nmap") == "Nmap installed successfully"
    lang.set_lang("es")
    assert lang.t("tool_name") == "Herramienta"


def test_cli_list():
    proc = subprocess.run(
        [sys.executable, "phi.py", "list", "scan"],
        capture_output=True,
        text=True,
        cwd=str(paths.REPO_ROOT),
    )
    assert proc.returncode == 0
    assert "nmap" in proc.stdout.lower()


def test_cli_info_unknown_tool():
    proc = subprocess.run(
        [sys.executable, "phi.py", "info", "no-existe"],
        capture_output=True,
        text=True,
        cwd=str(paths.REPO_ROOT),
    )
    assert proc.returncode == 1


def test_cli_help():
    proc = subprocess.run(
        [sys.executable, "phi.py", "--help"],
        capture_output=True,
        text=True,
        cwd=str(paths.REPO_ROOT),
    )
    assert proc.returncode == 0
