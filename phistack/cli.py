import argparse
import json
import shutil
import subprocess
import sys
import types

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from . import catalog, doctor, installer, menus, paths, state, style
from .lang import t, load_lang, set_lang, category_name, status_name

console = Console()


def _print_banner():
    config = _config()
    size = config.get("banner", "small")
    sys.stdout.write(style.render_banner(size) + "\n")
    sys.stdout.flush()


def _config():
    cfg = {}
    if paths.CONFIG_FILE.exists():
        try:
            with open(paths.CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, json.JSONDecodeError):
            cfg = {}
    return cfg


def _decorate(tool):
    name = tool.get("name", tool["id"])
    status_icon = {
        "active": "[green]●[/]",
        "legacy": "[yellow]●[/]",
        "obsolete": "[red]●[/]",
        "api": "[magenta]●[/]",
        "local": "[cyan]●[/]",
    }.get(tool.get("status"), "[grey]●[/]")
    mark = " [green]✓[/]" if state.is_installed(tool["id"]) else ""
    return f"{status_icon} {name}  ({tool['id']}){mark}"


def _tool_choices(tools):
    return [menus.Choice(value=tool["id"], name=_decorate(tool)) for tool in tools]


def _pick_tool(tools, message_key="select_tool"):
    if not tools:
        console.print(f"[yellow]{t('no_results', q='')}[/]")
        return None
    choice = menus.select(t(message_key), _tool_choices(tools))
    return next((x for x in tools if x["id"] == choice), None)


def _print_tool_table(tools):
    table = Table(title=t("analysis_title"))
    table.add_column(t("status"), no_wrap=True)
    table.add_column(t("category"))
    table.add_column(t("tool_id"))
    table.add_column(t("tool_name"))
    for tool in tools:
        icon = {
            "active": "[green]●[/]",
            "legacy": "[yellow]●[/]",
            "obsolete": "[red]●[/]",
            "api": "[magenta]●[/]",
            "local": "[cyan]●[/]",
        }.get(tool.get("status"), "●")
        table.add_row(
            f"{icon} {status_name(tool.get('status'))}",
            category_name(tool.get("category")),
            tool["id"],
            tool.get("name", tool["id"]),
        )
    console.print(table)


def cmd_list(args):
    tools = catalog.list_tools(category=args.category if args.category != "*" else None, status=args.status)
    _print_tool_table(tools)
    console.print(t("count_tools", n=len(tools)))


def cmd_search(args):
    results = catalog.search_tools(args.query)
    if not results:
        console.print(f"[yellow]{t('no_results', q=args.query)}[/]")
        return
    _print_tool_table(results)
    console.print(t("count_tools", n=len(results)))


def cmd_info(args):
    tool = catalog.get_tool(args.tool)
    if not tool:
        console.print(f"[red]{t('unknown_tool', tool=args.tool)}[/]")
        sys.exit(1)
    lines = [
        f"[bold]{tool.get('name', tool['id'])}[/] [grey]({tool['id']})[/]",
        "",
        f"[bold]{t('category')}:[/] {category_name(tool.get('category'))}",
        f"[bold]{t('status')}:[/] {status_name(tool.get('status'))}",
        f"[bold]{t('description')}:[/] {tool.get('desc_' + load_lang(), tool.get('desc_en', ''))}",
    ]
    note = tool.get("note_" + load_lang(), tool.get("note_en"))
    if note:
        lines.append(f"[bold]{t('note')}:[/] {note}")
    rep = tool.get("replacement")
    if rep:
        lines.append(f"[bold]{t('replacement')}:[/] {', '.join(rep)}")
    if tool.get("repo"):
        lines.append(f"[bold]{t('repository')}:[/] {tool['repo']}")
    if tool.get("run"):
        lines.append(f"[bold]{t('run_cmd')}:[/] phi run {tool['id']}")
    console.print(Panel("\n".join(lines), border_style="cyan"))
    console.print(f"[yellow]{t('warn_authorized')}[/]")


def cmd_install(args):
    tools = _resolve(args.tools, interactive=args.interactive)
    for tool in tools:
        if not tool:
            continue
        console.print(f"[cyan]{t('installing_tool', tool=tool.get('name', tool['id']))}[/]")
        ok, kind = installer.install_tool(tool)
        if kind == "already":
            console.print(f"[yellow]{tool.get('name', tool['id'])} {t('already_installed')}[/]")
        elif ok:
            console.print(f"[green]{t('install_ok', tool=tool.get('name', tool['id']))}[/]")
            if tool.get("run"):
                console.print(f"[cyan]{t('please_exec')}[/] [bold]phi run {tool['id']}[/]")
        else:
            console.print(f"[red]{t('install_fail', tool=tool.get('name', tool['id']))}[/]")
            sys.exit(1)


def cmd_remove(args):
    tools = _resolve(args.tools, interactive=args.interactive, installed_only=True)
    for tool in tools:
        if not tool:
            continue
        if not state.is_installed(tool["id"]) and not installer.installed_by_verify(tool):
            console.print(f"[yellow]{tool.get('name', tool['id'])} {t('not_installed_yet')}[/]")
            continue
        tool_name = tool.get("name", tool["id"])
        if not getattr(args, "yes", False):
            try:
                proceed = menus.confirm(t("confirm_remove", tool=tool_name))
            except (EOFError, KeyboardInterrupt):
                console.print(f"[yellow]{t('aborted')}[/]")
                return
            if not proceed:
                continue
        console.print(f"[cyan]{t('removing_tool', tool=tool.get('name', tool['id']))}[/]")
        if installer.remove_tool(tool):
            console.print(f"[green]{t('remove_ok', tool=tool.get('name', tool['id']))}[/]")
        else:
            console.print(f"[red]{t('remove_fail', tool=tool.get('name', tool['id']))}[/]")


def cmd_reinstall(args):
    for tool_id in args.tools:
        tool = catalog.get_tool(tool_id)
        if not tool:
            console.print(f"[red]{t('unknown_tool', tool=tool_id)}[/]")
            continue
        console.print(f"[cyan]{t('removing_tool', tool=tool.get('name', tool['id']))}[/]")
        installer.remove_tool(tool)
        console.print(f"[cyan]{t('installing_tool', tool=tool.get('name', tool['id']))}[/]")
        ok, kind = installer.install_tool(tool)
        if ok:
            console.print(f"[green]{t('install_ok', tool=tool.get('name', tool['id']))}[/]")
        else:
            console.print(f"[red]{t('install_fail', tool=tool.get('name', tool['id']))}[/]")


def cmd_run(args):
    tool = catalog.get_tool(args.tool)
    if not tool:
        console.print(f"[red]{t('unknown_tool', tool=args.tool)}[/]")
        sys.exit(1)
    run_cmd = tool.get("run", {}).get("cmd")
    if not run_cmd:
        console.print(f"[yellow]{t('not_installed_yet')}[/]")
        sys.exit(1)
    subprocess.run(installer.expand(run_cmd), shell=True)


def cmd_lang(args):
    if args.lang:
        set_lang(args.lang)
        console.print(f"[green]{t('language_set', lang=args.lang)}[/]")
        return
    lang = load_lang()
    choice = menus.select(
        t("choose_language"),
        [
            menus.Choice(value="es", name="Español" + (" (actual)" if lang == "es" else "")),
            menus.Choice(value="en", name="English" + (" (current)" if lang == "en" else "")),
        ],
    )
    set_lang(choice)
    console.print(f"[green]{t('language_set', lang=choice)}[/]")


def cmd_theme(args):
    choice = menus.select(
        t("theme_menu"),
        [
            menus.Choice(value="banner", name=t("banner_option")),
            menus.Choice(value="prompt", name=t("prompt_option")),
        ],
    )
    if choice == "banner":
        size = menus.select(
            t("banner_size"),
            [menus.Choice(value=s, name=s) for s in style.BANNER_SIZES],
        )
        style.set_banner(size)
        console.print(f"[green]{t('banner_set', size=size)}[/]")
    else:
        style_choice = menus.select(
            t("prompt_style"),
            [
                menus.Choice(value="default", name=t("prompt_default")),
                menus.Choice(value="phistack", name=t("prompt_phistack")),
                menus.Choice(value="custom", name=t("prompt_custom")),
            ],
        )
        if style_choice == "custom":
            username = menus.text(t("custom_username"), default="phistack")
            style.set_prompt_username(username)
            style.set_prompt("phistack")
        else:
            style.set_prompt(style_choice)
        style.apply_fish_prompt(style_choice)
        console.print(f"[green]{t('update_done')}[/]")


def cmd_doctor(args):
    ok = doctor.run_doctor()
    sys.exit(0 if ok else 1)


def cmd_update(args):
    console.print(f"[cyan]{t('update_check')}[/]")
    proc = subprocess.run(
        "git -C $PHISTACK pull --ff-only origin main".replace("$PHISTACK", str(paths.REPO_ROOT)),
        shell=True,
        text=True,
    )
    if proc.returncode == 0:
        console.print(f"[green]{t('update_done')}[/]")
    else:
        console.print(f"[yellow]{t('update_none')}[/]")


def cmd_uninstall(args):
    if not menus.confirm(t("confirm_uninstall"), default=False):
        return
    tools = catalog.list_tools()
    for tool in tools:
        if state.is_installed(tool["id"]):
            installer.remove_tool(tool)
    launcher = paths.BIN / "phi"
    if launcher.exists():
        launcher.unlink()
    shutil.rmtree(paths.CONFIG_DIR, ignore_errors=True)
    shutil.rmtree(paths.REPO_ROOT, ignore_errors=True)
    console.print(f"[green]{t('uninstall_done')}[/]")


def _resolve(ids, interactive=True, installed_only=False):
    tools = []
    for tool_id in ids:
        tool = catalog.get_tool(tool_id)
        if tool:
            tools.append(tool)
        else:
            console.print(f"[red]{t('unknown_tool', tool=tool_id)}[/]")
    if not tools and interactive:
        all_tools = catalog.list_tools()
        if installed_only:
            all_tools = [
                x
                for x in all_tools
                if state.is_installed(x["id"]) or installer.installed_by_verify(x)
            ]
        picked = _pick_tool(all_tools, "select_tool")
        if picked:
            tools.append(picked)
    return tools


def interactive():
    while True:
        _print_banner()
        lang = load_lang()
        choice = menus.select(
            t("main_menu"),
            [
                menus.Choice(value="install", name=t("install_tool")),
                menus.Choice(value="remove", name=t("remove_tool")),
                menus.Choice(value="reinstall", name=t("reinstall_tool")),
                menus.Choice(value="list", name=t("list_tools")),
                menus.Choice(value="search", name=t("search_tools")),
                menus.Choice(value="info", name=t("tool_info")),
                menus.Choice(value="theme", name=t("theme_style")),
                menus.Choice(value="doctor", name=t("doctor")),
                menus.Choice(value="lang", name=f"{t('language')} ({lang})"),
                menus.Choice(value="update", name=t("update_phistack")),
                menus.Choice(value="exit", name=t("exit")),
            ],
        )

        if choice == "install":
            cat = menus.select(
                t("select_category"),
                [menus.Choice(value="*", name=t("all_categories"))]
                + [
                    menus.Choice(value=c, name=category_name(c))
                    for c in catalog.category_ids()
                ],
            )
            tools = catalog.list_tools(category=cat)
            picked = _pick_tool(tools, "select_tool")
            if picked:
                cmd_install(types.SimpleNamespace(tools=[picked["id"]], interactive=False))
        elif choice == "remove":
            tools = [x for x in catalog.list_tools() if state.is_installed(x["id"])]
            picked = _pick_tool(tools, "select_tool")
            if picked:
                cmd_remove(types.SimpleNamespace(tools=[picked["id"]], interactive=False))
        elif choice == "reinstall":
            tools = [x for x in catalog.list_tools() if state.is_installed(x["id"])]
            picked = _pick_tool(tools, "select_tool")
            if picked:
                cmd_reinstall(types.SimpleNamespace(tools=[picked["id"]]))
        elif choice == "list":
            cmd_list(types.SimpleNamespace(category="*", status=None))
        elif choice == "search":
            query = menus.text(t("search_query"))
            cmd_search(types.SimpleNamespace(query=query))
        elif choice == "info":
            picked = _pick_tool(catalog.list_tools(), "select_tool")
            if picked:
                cmd_info(types.SimpleNamespace(tool=picked["id"]))
        elif choice == "theme":
            cmd_theme(None)
        elif choice == "doctor":
            cmd_doctor(None)
        elif choice == "lang":
            cmd_lang(types.SimpleNamespace(lang=None))
        elif choice == "update":
            cmd_update(None)
        else:
            break


def main():
    parser = argparse.ArgumentParser(prog="phi", description="PhiStack - Termux stack manager")
    parser.add_argument("--banner", action="store_true", help="Mostrar banner / Show banner")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="Listar herramientas / List tools")
    p_list.add_argument("category", nargs="?", default="*")
    p_list.add_argument("--status", default=None)
    p_list.set_defaults(func=cmd_list)

    p_search = sub.add_parser("search", help="Buscar herramienta / Search tools")
    p_search.add_argument("query")
    p_search.set_defaults(func=cmd_search)

    p_info = sub.add_parser("info", help="Info de herramienta / Tool info")
    p_info.add_argument("tool")
    p_info.set_defaults(func=cmd_info)

    p_install = sub.add_parser("install", help="Instalar / Install")
    p_install.add_argument("tools", nargs="*")
    p_install.add_argument("-i", "--interactive", action="store_true")
    p_install.set_defaults(func=cmd_install)

    p_remove = sub.add_parser("remove", help="Eliminar / Remove")
    p_remove.add_argument("tools", nargs="*")
    p_remove.add_argument("-i", "--interactive", action="store_true")
    p_remove.add_argument("-y", "--yes", action="store_true", help="Sin confirmación / Skip confirmation")
    p_remove.set_defaults(func=cmd_remove)

    p_re = sub.add_parser("reinstall", help="Reinstalar / Reinstall")
    p_re.add_argument("tools", nargs="*")
    p_re.set_defaults(func=cmd_reinstall)

    p_run = sub.add_parser("run", help="Ejecutar herramienta / Run tool")
    p_run.add_argument("tool")
    p_run.set_defaults(func=cmd_run)

    p_lang = sub.add_parser("lang", help="Idioma / Language")
    p_lang.add_argument("lang", nargs="?", choices=["es", "en"])
    p_lang.set_defaults(func=cmd_lang)

    p_theme = sub.add_parser("theme", help="Estilo / Theme")
    p_theme.set_defaults(func=cmd_theme)

    p_doctor = sub.add_parser("doctor", help="Diagnóstico / Diagnostics")
    p_doctor.set_defaults(func=cmd_doctor)

    p_update = sub.add_parser("update", help="Actualizar / Update")
    p_update.set_defaults(func=cmd_update)

    p_uninstall = sub.add_parser("uninstall", help="Desinstalar / Uninstall")
    p_uninstall.set_defaults(func=cmd_uninstall)

    args = parser.parse_args()

    missing = installer.need_dependencies()
    if missing:
        console.print(f"[yellow]Instalando dependencias: {', '.join(missing)}[/]")
        installer.ensure_dependencies()

    if args.banner or args.command is None:
        _print_banner()
        if args.command is None:
            interactive()
        return

    args.func(args)


def cli():
    sys.exit(main())
