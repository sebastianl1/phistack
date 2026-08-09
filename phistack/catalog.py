import json
import re

from . import paths


class CatalogError(Exception):
    pass


def _load():
    try:
        with open(paths.CATALOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    except OSError as exc:
        raise CatalogError(f"No se puede leer el catálogo: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise CatalogError(f"Catálogo JSON inválido: {exc}") from exc


def load_catalog():
    data = _load()
    tools = data.get("tools", [])
    ids = {}
    for tool in tools:
        tool_id = tool.get("id")
        if not tool_id:
            raise CatalogError("Herramienta sin 'id' en el catálogo")
        if tool_id in ids:
            raise CatalogError(f"id duplicado en el catálogo: {tool_id}")
        ids[tool_id] = tool
    return data


def categories():
    return load_catalog().get("categories", {})


def list_tools(category=None, status=None):
    tools = load_catalog().get("tools", [])
    if category and category != "*":
        tools = [t for t in tools if t.get("category") == category]
    if status:
        tools = [t for t in tools if t.get("status") == status]
    return tools


def get_tool(tool_id):
    for tool in load_catalog().get("tools", []):
        if tool.get("id") == tool_id:
            return tool
    return None


def search_tools(query):
    q = re.escape(query.strip().lower())
    pattern = re.compile(q)
    results = []
    for tool in load_catalog().get("tools", []):
        haystack = " ".join(
            [
                tool.get("id", ""),
                tool.get("name", ""),
                tool.get("desc_es", ""),
                tool.get("desc_en", ""),
                tool.get("note_es", ""),
                tool.get("note_en", ""),
            ]
        ).lower()
        if pattern.search(haystack):
            results.append(tool)
    return results


def category_ids():
    return list(load_catalog().get("categories", {}).keys())


def validate():
    data = load_catalog()
    errors = []
    allowed_methods = {"pkg", "git", "pip", "run", "download", "launcher"}
    for tool in data.get("tools", []):
        tool_id = tool.get("id")
        if tool.get("category") not in data.get("categories", {}):
            errors.append(f"{tool_id}: categoría inválida '{tool.get('category')}'")
        if tool.get("status") not in {"active", "legacy", "obsolete", "api", "local"}:
            errors.append(f"{tool_id}: estado inválido '{tool.get('status')}'")
        for step in tool.get("install", []):
            if step.get("method") not in allowed_methods:
                errors.append(f"{tool_id}: método inválido '{step.get('method')}'")
    return errors
