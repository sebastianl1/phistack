#!/usr/bin/env python3
"""Genera docs/lang/{es,en,pt,fr,de,zh}.js a partir de tools/i18n_part1.json y i18n_part2.json.

Uso: python3 tools/build_lang.py
Valida que todas las claves existan en los 6 idiomas antes de escribir.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "lang"
PARTS = [
    ROOT / "tools" / "i18n_part1.json",
    ROOT / "tools" / "i18n_part2.json",
]
LANGS = ["es", "en", "pt", "fr", "de", "zh"]


def main():
    data = {}
    for part in PARTS:
        with open(part, encoding="utf-8") as f:
            data.update(json.load(f))

    for key, values in data.items():
        if len(values) != 6:
            raise SystemExit(f"clave {key}: esperaba 6 idiomas, tengo {len(values)}")

    OUT.mkdir(parents=True, exist_ok=True)
    for idx, lang in enumerate(LANGS):
        body = {key: values[idx] for key, values in data.items()}
        js = "window.I18N = " + json.dumps(body, ensure_ascii=False, indent=2) + ";\n"
        (OUT / f"{lang}.js").write_text(js, encoding="utf-8")
        print(f"docs/lang/{lang}.js -> {len(body)} claves")


if __name__ == "__main__":
    main()
