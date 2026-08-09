import argparse
import json
import shutil
import subprocess
import sys
import types

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from . import catalog, doctor, installer, menus, paths, presets, state, style
from .lang import t, load_lang, set_lang, category_name, status_name

console = Console()

STATUS_ICON = {
    "active": "[green]●[/]",
    "legacy": "[yellow]●[/]",
    "obsolete": "[red]●[/]",
    "api": "[magenta]●[/]",
    "local": "[cyan]●[/]",
}


def _config():
    cfg = {}
    if paths.CONFIG_FILE.exists():
        try:
            with open(paths.CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, json.JSONDecodeError):
            cfg = {}
    return cfg


def _print_banner():
    config = _config()
    size = config.get("banner", "small")
    sys.stdout.write(style.render_banner(size) + "\n")
    sys.stdout.flush()


def _installed_mark(tool):
    if state.is_installed(tool["id"]) or installer.installed_by_verify(tool):
        return " [green]✓[/]"
    return ""


def _print_tool_table(tools, group=False, show_desc=False):
    if group:
        for cat in catalog.category_ids():
            rows = [x for x in tools if x.get("category") == cat]
            if not rows:
                continue
            table = Table(title=f"[bold]{category_name(cat)}[/]", box=None, pad_edge=False)
            table.add_column(t("status"), no_wrap=True)
            table.add_column(t("tool_id"))
            table.add_column(t("tool_name"))
            table.add_column(t("source"), no_wrap=True)
            for tool in rows:
                table.add_row(
                    f"{STATUS_ICON.get(tool.get('status'), '●')} {status_name(tool.get('status'))}",
                    tool["id"],
                    tool.get("name", tool["id"]) + _installed_mark(tool),
                    tool.get("source", ""),
                )
            console.print(table)
            console.print()
        return
    lang = load_lang()
    table = Table(box=None, pad_edge=False, show_header=True, header_style="bold")
    table.add_column(t("tool_id"), no_wrap=True, style="bold")
    table.add_column(t("tool_name"))
    table.add_column(t("category"), no_wrap=True)
    table.add_column(t("status"), no_wrap=True)
    table.add_column(t("source"), no_wrap=True)
    if show_desc:
        table.add_column(t("description"))
    cat_order = catalog.category_ids()
    ordered = sorted(
        tools,
        key=lambda x: (
            cat_order.index(x.get("category")) if x.get("category") in cat_order else 99,
            x.get("name", x["id"]),
        ),
    )
    for tool in ordered:
        row = [
            tool["id"],
            tool.get("name", tool["id"]) + _installed_mark(tool),
            category_name(tool.get("category")),
            f"{STATUS_ICON.get(tool.get('status'), '●')} {status_name(tool.get('status'))}",
            tool.get("source", ""),
        ]
        if show_desc:
            row.append(tool.get("desc_" + lang, tool.get("desc_en", "")))
        table.add_row(*row)
    console.print(table)


def cmd_list(args):
    tools = catalog.list_tools(
        category=args.category if args.category and args.category != "*" else None,
        status=args.status,
    )
    if args.installed:
        tools = [x for x in tools if state.is_installed(x["id"]) or installer.installed_by_verify(x)]
    if args.source:
        tools = [x for x in tools if x.get("source") == args.source]
    if args.detail:
        for tool in tools:
            cmd_info(types.SimpleNamespace(tool=tool["id"]))
        return
    show_desc = bool(args.category and args.category != "*")
    _print_tool_table(tools, group=args.group, show_desc=show_desc)
    cats = len({x.get("category") for x in tools})
    console.print(f"[dim]{t('list.tools_count', n=len(tools), c=cats)}[/]")


def cmd_search(args):
    results = catalog.search_tools(args.query)
    if not results:
        console.print(f"[yellow]{t('no_results', q=args.query)}[/]")
        return
    _print_tool_table(results, group=False)
    console.print(f"[dim]{t('list.tools_count', n=len(results), c=len({x.get('category') for x in results}))}[/]")


def cmd_info(args):
    tool = catalog.get_tool(args.tool)
    if not tool:
        console.print(f"[red]{t('unknown_tool', tool=args.tool)}[/]")
        sys.exit(1)
    lang = load_lang()
    lines = [
        f"[bold]{tool.get('name', tool['id'])}[/] [grey]({tool['id']})[/]",
        "",
        f"[bold]{t('category')}:[/] {category_name(tool.get('category'))}",
        f"[bold]{t('status')}:[/] {status_name(tool.get('status'))}",
        f"[bold]{t('source')}:[/] {tool.get('source', '')}",
        f"[bold]{t('description')}:[/] {tool.get('desc_' + lang, tool.get('desc_en', ''))}",
    ]
    note = tool.get("note_" + lang, tool.get("note_en"))
    if note:
        lines.append(f"[bold]{t('note')}:[/] {note}")
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
        name = tool.get("name", tool["id"])
        console.print(f"[cyan]{t('installing_tool', tool=name)}[/]")
        ok, kind = installer.install_tool(tool)
        if kind == "already":
            console.print(f"[yellow]{name} {t('already_installed')}[/]")
        elif ok:
            console.print(f"[green]{t('install_ok', tool=name)}[/]")
            if tool.get("run"):
                console.print(f"[cyan]{t('please_exec')}[/] [bold]phi run {tool['id']}[/]")
        else:
            console.print(f"[red]{t('install_fail', tool=name)}[/]")
            sys.exit(1)


def cmd_remove(args):
    tools = _resolve(args.tools, interactive=args.interactive, installed_only=True)
    for tool in tools:
        if not tool:
            continue
        name = tool.get("name", tool["id"])
        if not state.is_installed(tool["id"]) and not installer.installed_by_verify(tool):
            console.print(f"[yellow]{name} {t('not_installed_yet')}[/]")
            continue
        if not getattr(args, "yes", False):
            try:
                proceed = menus.confirm(t("confirm_remove", tool=name))
            except (EOFError, KeyboardInterrupt):
                console.print(f"[yellow]{t('aborted')}[/]")
                return
            if not proceed:
                continue
        console.print(f"[cyan]{t('removing_tool', tool=name)}[/]")
        if installer.remove_tool(tool):
            console.print(f"[green]{t('remove_ok', tool=name)}[/]")
        else:
            console.print(f"[red]{t('remove_fail', tool=name)}[/]")


def cmd_reinstall(args):
    for tool_id in args.tools:
        tool = catalog.get_tool(tool_id)
        if not tool:
            console.print(f"[red]{t('unknown_tool', tool=tool_id)}[/]")
            continue
        name = tool.get("name", tool["id"])
        console.print(f"[cyan]{t('removing_tool', tool=name)}[/]")
        installer.remove_tool(tool)
        console.print(f"[cyan]{t('installing_tool', tool=name)}[/]")
        ok, kind = installer.install_tool(tool)
        if ok:
            console.print(f"[green]{t('install_ok', tool=name)}[/]")
        else:
            console.print(f"[red]{t('install_fail', tool=name)}[/]")


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
        styles = presets.prompt_styles()
        picked = menus.select(t("term.choose_prompt"), [menus.Choice(value=s, name=s) for s in styles])
        presets.set_prompt(picked)
        console.print(f"[green]{t('term.prompt_ok', style=picked)}[/]")


def cmd_doctor(args):
    ok = doctor.run_doctor()
    sys.exit(0 if ok else 1)


def cmd_update(args):
    console.print(f"[cyan]{t('update_check')}[/]")
    proc = subprocess.run(
        f"git -C {paths.REPO_ROOT} pull --ff-only origin main",
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
    for tool in catalog.list_tools():
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


def _pick_tool(tools, message_key="select_tool"):
    if not tools:
        console.print(f"[yellow]{t('no_results', q='')}[/]")
        return None
    choices = [
        menus.Choice(
            value=tool["id"],
            name=f"{STATUS_ICON.get(tool.get('status'), '●')} {tool.get('name', tool['id'])}  ({tool['id']}){_installed_mark(tool)}",
        )
        for tool in tools
    ]
    if len(tools) > 12:
        choice = menus.fuzzy_select(t(message_key), choices)
    else:
        choice = menus.select(t(message_key), choices)
    return next((x for x in tools if x["id"] == choice), None)


# ---------------- Laboratorio: Terminal ----------------

def cmd_term_list(args):
    console.print(f"[bold cyan]{t('term.presets')}[/]")
    for p in presets.term_presets():
        console.print(f"  [cyan]●[/] {p}")
    console.print(f"[bold cyan]{t('term.banner')}:[/] {', '.join(presets.banner_styles())}")
    console.print(f"[bold cyan]{t('term.prompt')}:[/] {', '.join(presets.prompt_styles())}")
    console.print(f"[bold cyan]{t('term.shell')}:[/] {', '.join(presets.shell_presets())}")


def cmd_term_set(args):
    try:
        copied = presets.apply_term_preset(args.preset)
    except FileNotFoundError:
        console.print(f"[red]{t('invalid_option')}[/]")
        sys.exit(1)
    console.print(f"[green]{t('term.set_ok', preset=args.preset)}[/] ({', '.join(copied)})")


def cmd_term_banner(args):
    styles = presets.banner_styles()
    style = args.style or menus.select(
        t("term.choose_banner"),
        [menus.Choice(value=s, name=s) for s in styles],
    )
    if presets.set_banner(style):
        console.print(f"[green]{t('term.banner_ok', style=style)}[/]")
    else:
        console.print(f"[red]{t('invalid_option')}[/]")


def cmd_term_prompt(args):
    styles = presets.prompt_styles()
    picked = args.style or menus.select(
        t("term.choose_prompt"),
        [menus.Choice(value=s, name=s) for s in styles],
    )
    if presets.set_prompt(picked):
        console.print(f"[green]{t('term.prompt_ok', style=picked)}[/]")
    else:
        console.print(f"[red]{t('invalid_option')}[/]")


def cmd_term_shell(args):
    presets_list = presets.shell_presets()
    picked = args.shell or menus.select(
        t("term.choose_shell"),
        [menus.Choice(value=s, name=s) for s in presets_list],
    )
    try:
        changed = presets.set_shell(picked)
    except FileNotFoundError:
        console.print(f"[red]{t('invalid_option')}[/]")
        sys.exit(1)
    console.print(f"[green]{t('term.shell_ok', style=picked)}[/] ({', '.join(changed)})")


def cmd_term_save(args):
    name = args.name or menus.text(t("term.save_name"), default="mi-preset")
    if not name:
        return
    term_copied = presets.save_term(name)
    shell_copied = presets.save_shell(name)
    console.print(f"[green]{t('term.saved', name=name)}[/] ({', '.join(term_copied + shell_copied)})")


def cmd_term_edit(args):
    editor = _editor()
    targets = {
        "termux": str(presets.TERMUX_HOME / "termux.properties"),
        "colors": str(presets.TERMUX_HOME / "colors.properties"),
        "fish": str(presets.FISH_CONFIG),
        "prompt": str(presets.FISH_FUNC),
        "banner": str(presets.ETC_MOTD),
    }
    part = args.part or menus.select(
        t("term.edit"),
        [menus.Choice(value=k, name=k) for k in targets],
    )
    if part in targets:
        subprocess.run([editor, targets[part]])
    else:
        console.print(f"[red]{t('invalid_option')}[/]")


def _editor():
    return __import__("os").environ.get("EDITOR", "nvim")


# ---------------- Laboratorio: IDE ----------------

def cmd_ide_list(args):
    console.print(f"[bold cyan]{t('menu.ide')}[/]")
    for p in presets.ide_presets():
        console.print(f"  [cyan]●[/] {p}")


def cmd_ide_install(args):
    presets_list = presets.ide_presets()
    picked = args.preset or menus.select(
        t("ide.choose_preset"),
        [menus.Choice(value=s, name=s) for s in presets_list],
    )
    try:
        presets.ide_install(picked)
    except FileNotFoundError:
        console.print(f"[red]{t('invalid_option')}[/]")
        sys.exit(1)
    console.print(f"[green]{t('ide.install_ok', preset=picked)}[/]")


def cmd_ide_edit(args):
    subprocess.run([_editor(), str(presets.NVIM_CONFIG)])


def cmd_ide_backup(args):
    backup = presets.ide_backup()
    if backup:
        console.print(f"[green]{t('ide.backup_ok', path=str(backup))}[/]")
    else:
        console.print(f"[yellow]{t('not_installed_yet')}[/]")


# ---------------- Modo interactivo ----------------

def interactive():
    while True:
        _print_banner()
        lang = load_lang()
        choice = menus.select(
            t("main_menu"),
            [
                menus.Choice(value="lab", name=f"🧪 {t('menu.lab')}"),
                menus.Choice(value="install", name=f"🛠️  {t('install_tool')}"),
                menus.Choice(value="remove", name=f"🗑️  {t('remove_tool')}"),
                menus.Choice(value="list", name=f"📋 {t('list_tools')}"),
                menus.Choice(value="search", name=f"🔍 {t('search_tools')}"),
                menus.Choice(value="info", name=f"ℹ️  {t('tool_info')}"),
                menus.Choice(value="doctor", name=f"🩺 {t('doctor')}"),
                menus.Choice(value="lang", name=f"🌐 {t('language')} ({lang})"),
                menus.Choice(value="update", name=f"🔄 {t('update_phistack')}"),
                menus.Choice(value="exit", name=t("exit")),
            ],
        )

        if choice == "lab":
            _interactive_lab()
        elif choice == "install":
            cat = menus.select(
                t("select_category"),
                [menus.Choice(value="*", name=t("all_categories"))]
                + [menus.Choice(value=c, name=category_name(c)) for c in catalog.category_ids()],
            )
            tools = catalog.list_tools(category=cat if cat != "*" else None)
            picked = _pick_tool(tools)
            if picked:
                cmd_install(types.SimpleNamespace(tools=[picked["id"]], interactive=False))
        elif choice == "remove":
            tools = [x for x in catalog.list_tools() if state.is_installed(x["id"]) or installer.installed_by_verify(x)]
            picked = _pick_tool(tools)
            if picked:
                cmd_remove(types.SimpleNamespace(tools=[picked["id"]], interactive=False, yes=False))
        elif choice == "list":
            cmd_list(types.SimpleNamespace(category="*", status=None, installed=False, source=None, detail=False, group=False))
        elif choice == "search":
            query = menus.text(t("search_query"))
            cmd_search(types.SimpleNamespace(query=query))
        elif choice == "info":
            picked = _pick_tool(catalog.list_tools())
            if picked:
                cmd_info(types.SimpleNamespace(tool=picked["id"]))
        elif choice == "doctor":
            cmd_doctor(None)
        elif choice == "lang":
            cmd_lang(types.SimpleNamespace(lang=None))
        elif choice == "update":
            cmd_update(None)
        else:
            break


def _interactive_lab():
    while True:
        choice = menus.select(
            t("menu.lab"),
            [
                menus.Choice(value="term", name=f"🖥️  {t('menu.term')}"),
                menus.Choice(value="ide", name=f"📝 {t('menu.ide')}"),
                menus.Choice(value="back", name=t("back")),
            ],
        )
        if choice == "term":
            _interactive_term()
        elif choice == "ide":
            _interactive_ide()
        else:
            return


def _interactive_term():
    choice = menus.select(
        t("menu.term"),
        [
            menus.Choice(value="preset", name=t("term.presets")),
            menus.Choice(value="banner", name=t("term.banner")),
            menus.Choice(value="prompt", name=t("term.prompt")),
            menus.Choice(value="shell", name=t("term.shell")),
            menus.Choice(value="save", name=t("term.save")),
            menus.Choice(value="edit", name=t("term.edit")),
            menus.Choice(value="back", name=t("back")),
        ],
    )
    if choice == "preset":
        presets_list = presets.term_presets()
        picked = menus.select(t("term.choose_preset"), [menus.Choice(value=s, name=s) for s in presets_list])
        cmd_term_set(types.SimpleNamespace(preset=picked))
    elif choice == "banner":
        cmd_term_banner(types.SimpleNamespace(style=None))
    elif choice == "prompt":
        cmd_term_prompt(types.SimpleNamespace(style=None))
    elif choice == "shell":
        cmd_term_shell(types.SimpleNamespace(shell=None))
    elif choice == "save":
        cmd_term_save(types.SimpleNamespace(name=None))
    elif choice == "edit":
        cmd_term_edit(types.SimpleNamespace(part=None))


def _interactive_ide():
    choice = menus.select(
        t("menu.ide"),
        [
            menus.Choice(value="install", name=t("ide.choose_preset")),
            menus.Choice(value="edit", name=t("ide.edit")),
            menus.Choice(value="backup", name=t("ide.backup")),
            menus.Choice(value="back", name=t("back")),
        ],
    )
    if choice == "install":
        cmd_ide_install(types.SimpleNamespace(preset=None))
    elif choice == "edit":
        cmd_ide_edit(None)
    elif choice == "backup":
        cmd_ide_backup(None)


# ---------------- Main ----------------

def main():
    parser = argparse.ArgumentParser(prog="phi", description="PhiStack - Laboratorio Termux")
    parser.add_argument("--banner", action="store_true", help="Mostrar banner / Show banner")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="Listar herramientas / List tools")
    p_list.add_argument("category", nargs="?", default="*")
    p_list.add_argument("--status", default=None)
    p_list.add_argument("--installed", action="store_true")
    p_list.add_argument("--source", default=None, choices=["vendor", "pkg", "pip", "download"])
    p_list.add_argument("--group", action="store_true", help="Agrupar por categoría / Group by category")
    p_list.add_argument("--detail", action="store_true")
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

    # phi term
    p_term = sub.add_parser("term", help="Laboratorio de terminal / Terminal lab")
    term_sub = p_term.add_subparsers(dest="term_cmd")
    term_sub.add_parser("list", help="Listar presets / List presets").set_defaults(func=cmd_term_list)
    ps = term_sub.add_parser("set", help="Aplicar preset / Apply preset")
    ps.add_argument("preset")
    ps.set_defaults(func=cmd_term_set)
    pb = term_sub.add_parser("banner", help="Banner de inicio / Login banner")
    pb.add_argument("style", nargs="?")
    pb.set_defaults(func=cmd_term_banner)
    pp = term_sub.add_parser("prompt", help="Prompt de fish / Fish prompt")
    pp.add_argument("style", nargs="?")
    pp.set_defaults(func=cmd_term_prompt)
    psh = term_sub.add_parser("shell", help="Config de shell / Shell config")
    psh.add_argument("shell", nargs="?")
    psh.set_defaults(func=cmd_term_shell)
    psv = term_sub.add_parser("save", help="Guardar config como preset / Save as preset")
    psv.add_argument("name", nargs="?")
    psv.set_defaults(func=cmd_term_save)
    pe = term_sub.add_parser("edit", help="Editar config instalada / Edit installed config")
    pe.add_argument("part", nargs="?")
    pe.set_defaults(func=cmd_term_edit)

    # phi ide
    p_ide = sub.add_parser("ide", help="Laboratorio de IDE / IDE lab")
    ide_sub = p_ide.add_subparsers(dest="ide_cmd")
    ide_sub.add_parser("list", help="Listar presets / List presets").set_defaults(func=cmd_ide_list)
    pi = ide_sub.add_parser("install", help="Instalar preset / Install preset")
    pi.add_argument("preset", nargs="?")
    pi.set_defaults(func=cmd_ide_install)
    ide_sub.add_parser("edit", help="Editar config / Edit config").set_defaults(func=cmd_ide_edit)
    ide_sub.add_parser("backup", help="Respaldar config / Backup config").set_defaults(func=cmd_ide_backup)

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
