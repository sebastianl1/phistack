import shutil
import sys

from rich.console import Console
from rich.table import Table

from .lang import t
from . import paths


def _check(console, name_key, ok, detail=""):
    ok = bool(ok)
    label = t(name_key)
    icon = "[green]✓[/]" if ok else "[red]✗[/]"
    status = t("doctor_ok") if ok else t("doctor_fail")
    return ok, f"{icon} {label}: {status} {detail}"


def run_doctor():
    console = Console()
    console.print(f"[bold cyan]{t('doctor_check')}[/]")
    table = Table(show_header=False, box=None, pad_edge=False)
    checks = []

    ok, row = _check(console, "doctor_python", sys.version_info >= (3, 7), f"({sys.version.split()[0]})")
    checks.append(ok)
    table.add_row(row)

    ok, row = _check(console, "doctor_pip", shutil.which("pip3") or shutil.which("pip"))
    checks.append(ok)
    table.add_row(row)

    ok, row = _check(console, "doctor_git", bool(shutil.which("git")))
    checks.append(ok)
    table.add_row(row)

    ok, row = _check(console, "doctor_pkg", bool(shutil.which("pkg")))
    checks.append(ok)
    table.add_row(row)

    try:
        import InquirerPy  # noqa: F401

        deps_ok = True
    except ImportError:
        deps_ok = False
    try:
        import rich  # noqa: F401
    except ImportError:
        deps_ok = False
    ok, row = _check(console, "doctor_deps", deps_ok)
    checks.append(ok)
    table.add_row(row)

    console.print(table)
    console.print(
        t("doctor_summary", ok=sum(checks), total=len(checks))
    )
    return all(checks)
