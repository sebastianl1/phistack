import json

from . import paths

DEFAULT_LANG = "es"

STRINGS = {
    "app_name": {"es": "PhiStack", "en": "PhiStack"},
    "tagline": {
        "es": "Gestor de stack para Termux",
        "en": "Termux stack manager",
    },
    "welcome": {
        "es": "Bienvenido a PhiStack",
        "en": "Welcome to PhiStack",
    },
    "main_menu": {
        "es": "Menú principal de PhiStack",
        "en": "PhiStack main menu",
    },
    "install_tool": {"es": "Instalar herramienta", "en": "Install tool"},
    "remove_tool": {"es": "Eliminar herramienta", "en": "Remove tool"},
    "reinstall_tool": {"es": "Reinstalar herramienta", "en": "Reinstall tool"},
    "list_tools": {"es": "Listar herramientas", "en": "List tools"},
    "search_tools": {"es": "Buscar herramienta", "en": "Search tool"},
    "tool_info": {"es": "Información de herramienta", "en": "Tool info"},
    "theme_style": {"es": "Estilo (banner / prompt)", "en": "Style (banner / prompt)"},
    "language": {"es": "Idioma", "en": "Language"},
    "doctor": {"es": "Chequeo de sistema (doctor)", "en": "System check (doctor)"},
    "update_phistack": {"es": "Actualizar PhiStack", "en": "Update PhiStack"},
    "uninstall_phistack": {"es": "Desinstalar PhiStack", "en": "Uninstall PhiStack"},
    "exit": {"es": "Salir", "en": "Exit"},
    "select_category": {"es": "Selecciona una categoría", "en": "Select a category"},
    "all_categories": {"es": "Todas las categorías", "en": "All categories"},
    "select_tool": {"es": "Selecciona una herramienta", "en": "Select a tool"},
    "select_tools": {
        "es": "Selecciona las herramientas a instalar",
        "en": "Select the tools to install",
    },
    "confirm_remove": {
        "es": "¿Seguro que quieres eliminar {tool}?",
        "en": "Are you sure you want to remove {tool}?",
    },
    "confirm_uninstall": {
        "es": "¿Seguro que quieres desinstalar PhiStack?",
        "en": "Are you sure you want to uninstall PhiStack?",
    },
    "installed": {"es": "instalada", "en": "installed"},
    "not_installed": {"es": "no instalada", "en": "not installed"},
    "install_ok": {"es": "{tool} instalada correctamente", "en": "{tool} installed successfully"},
    "install_fail": {"es": "Error al instalar {tool}", "en": "Failed to install {tool}"},
    "remove_ok": {"es": "{tool} eliminada correctamente", "en": "{tool} removed successfully"},
    "remove_fail": {"es": "Error al eliminar {tool}", "en": "Failed to remove {tool}"},
    "already_installed": {"es": "ya está instalada", "en": "is already installed"},
    "not_installed_yet": {
        "es": "no está instalada",
        "en": "is not installed yet",
    },
    "unknown_tool": {"es": "Herramienta desconocida: {tool}", "en": "Unknown tool: {tool}"},
    "invalid_option": {"es": "Opción inválida", "en": "Invalid option"},
    "invalid_arg": {"es": "Argumento inválido", "en": "Invalid argument"},
    "search_query": {"es": "Término de búsqueda", "en": "Search term"},
    "no_results": {"es": "Sin resultados para '{q}'", "en": "No results for '{q}'"},
    "category": {"es": "Categoría", "en": "Category"},
    "status": {"es": "Estado", "en": "Status"},
    "description": {"es": "Descripción", "en": "Description"},
    "note": {"es": "Nota", "en": "Note"},
    "replacement": {"es": "Sugerencia de reemplazo", "en": "Suggested replacement"},
    "repository": {"es": "Repositorio", "en": "Repository"},
    "install_cmd": {"es": "Instalar", "en": "Install"},
    "remove_cmd": {"es": "Eliminar", "en": "Remove"},
    "run_cmd": {"es": "Ejecutar", "en": "Run"},
    "status_active": {"es": "Activa", "en": "Active"},
    "status_legacy": {"es": "Legacy", "en": "Legacy"},
    "status_obsolete": {"es": "Obsoleta", "en": "Obsolete"},
    "status_api": {"es": "Requiere API", "en": "Requires API"},
    "status_local": {"es": "Local/Regional", "en": "Local/Regional"},
    "warn_authorized": {
        "es": "Uso autorizado únicamente. No pruebes sistemas que no te pertenecen o sin permiso explícito.",
        "en": "Authorized use only. Do not test systems you do not own or without explicit permission.",
    },
    "choose_language": {
        "es": "Elige el idioma / Choose the language",
        "en": "Elige el idioma / Choose the language",
    },
    "language_set": {
        "es": "Idioma configurado: {lang}",
        "en": "Language set: {lang}",
    },
    "theme_menu": {
        "es": "¿Qué quieres configurar?",
        "en": "What do you want to configure?",
    },
    "banner_option": {"es": "Banner", "en": "Banner"},
    "prompt_option": {"es": "Prompt de fish", "en": "Fish prompt"},
    "banner_size": {"es": "Tamaño del banner", "en": "Banner size"},
    "prompt_style": {"es": "Estilo del prompt", "en": "Prompt style"},
    "prompt_default": {"es": "Por defecto", "en": "Default"},
    "prompt_phistack": {"es": "PhiStack", "en": "PhiStack"},
    "prompt_custom": {"es": "Personalizado", "en": "Custom"},
    "custom_username": {"es": "Nombre de usuario para el prompt", "en": "Username for the prompt"},
    "banner_set": {
        "es": "Banner configurado: {size}",
        "en": "Banner set: {size}",
    },
    "doctor_title": {"es": "Diagnóstico de PhiStack", "en": "PhiStack diagnostics"},
    "doctor_ok": {"es": "OK", "en": "OK"},
    "doctor_fail": {"es": "FALLO", "en": "FAIL"},
    "doctor_python": {"es": "Python", "en": "Python"},
    "doctor_pip": {"es": "pip", "en": "pip"},
    "doctor_git": {"es": "git", "en": "git"},
    "doctor_pkg": {"es": "pkg (Termux)", "en": "pkg (Termux)"},
    "doctor_deps": {"es": "Dependencias Python", "en": "Python dependencies"},
    "doctor_check": {"es": "Verificando sistema...", "en": "Checking system..."},
    "doctor_summary": {
        "es": "{ok} de {total} chequeos correctos",
        "en": "{ok} of {total} checks passed",
    },
    "update_check": {
        "es": "Comprobando actualizaciones...",
        "en": "Checking for updates...",
    },
    "update_none": {
        "es": "Ya estás en la última versión",
        "en": "You are already up to date",
    },
    "update_done": {
        "es": "PhiStack actualizado",
        "en": "PhiStack updated",
    },
    "uninstall_done": {
        "es": "PhiStack desinstalado",
        "en": "PhiStack uninstalled",
    },
    "back": {"es": "← Volver", "en": "← Back"},
    "installing_tool": {
        "es": "Instalando {tool}...",
        "en": "Installing {tool}...",
    },
    "removing_tool": {
        "es": "Eliminando {tool}...",
        "en": "Removing {tool}...",
    },
    "please_exec": {
        "es": "Instalación finalizada. Ejecuta:",
        "en": "Installation finished. Execute:",
    },
    "count_tools": {
        "es": "{n} herramientas",
        "en": "{n} tools",
    },
    "analysis_title": {
        "es": "Análisis de herramientas (activas / legacy / obsoletas)",
        "en": "Tools analysis (active / legacy / obsolete)",
    },
    "tool_name": {"es": "Herramienta", "en": "Tool"},
    "tool_id": {"es": "ID", "en": "ID"},
    "aborted": {"es": "Operación cancelada", "en": "Operation aborted"},
}

CATEGORIES = {
    "osint": {"es": "OSINT / Recolección", "en": "OSINT / Recon"},
    "scan": {"es": "Escaneo", "en": "Scanning"},
    "web": {"es": "Web", "en": "Web"},
    "exploit": {"es": "Explotación", "en": "Exploitation"},
    "crack": {"es": "Contraseñas", "en": "Password cracking"},
    "phishing": {"es": "Phishing / Social", "en": "Phishing / Social"},
    "wireless": {"es": "Red / Wireless", "en": "Network / Wireless"},
    "forense": {"es": "Forense / Metadatos", "en": "Forensics / Metadata"},
    "utils": {"es": "Utilidades", "en": "Utilities"},
}


def load_lang():
    try:
        with open(paths.CONFIG_FILE, encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("lang", DEFAULT_LANG)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_LANG


def set_lang(lang):
    paths.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    cfg = {}
    if paths.CONFIG_FILE.exists():
        try:
            with open(paths.CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, json.JSONDecodeError):
            cfg = {}
    cfg["lang"] = lang
    with open(paths.CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def t(key, language=None, **fmt):
    lang = language or load_lang()
    table = STRINGS.get(key, {})
    if isinstance(table, dict):
        value = table.get(lang, table.get(DEFAULT_LANG, key))
    else:
        value = table
    if fmt:
        value = value.format(**fmt)
    return value


def category_name(cat_id, lang=None):
    lang = lang or load_lang()
    entry = CATEGORIES.get(cat_id, {})
    return entry.get(lang, entry.get(DEFAULT_LANG, cat_id))


def status_name(status, lang=None):
    lang = lang or load_lang()
    key = {
        "active": "status_active",
        "legacy": "status_legacy",
        "obsolete": "status_obsolete",
        "api": "status_api",
        "local": "status_local",
    }.get(status, "status_legacy")
    return t(key, language=lang)
