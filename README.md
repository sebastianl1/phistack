# PhiStack 🐍

**Laboratorio Termux** — estructura tu terminal de Android para desarrollo de software y ciberseguridad, con un catálogo curado y funcional de herramientas, presets de terminal e IDE. Bilingüe ES/EN.

> Uso autorizado únicamente. Muchas herramientas son para pruebas de seguridad.
> No pruebes sistemas que no te pertenecen o sin permiso explícito.

## Características / Features

- **Catálogo curado de 41 herramientas funcionales**, organizadas en 9 categorías (OSINT, escaneo, web, explotación, contraseñas, phishing, red, forense, utilidades).
- **Código vendorizado**: las herramientas de script (Python/bash) viven **dentro del repo** en `lab/tools/<id>/` — sin depender de `git clone` de terceros. Las compiladas se instalan vía `pkg` (marcadas "sistema").
- **Menús interactivos** con [InquirerPy](https://github.com/kazhala/InquirerPy): select, fuzzy, checkbox, confirm.
- **Modo interactivo y CLI**: `phi` abre el menú; `phi install <tool>` por línea de comandos.
- **Laboratorio de terminal** (`phi term`): presets de banner aleatorio de login, prompt de fish, colores y fuente. Elige, personaliza o guarda tu propia config.
- **Laboratorio de IDE** (`phi ide`): presets de nvim (AstroVim + variantes). Instala, edita y respalda.
- **Banner fractal**: conjunto de Mandelbrot completo en silueta 2 tonos (ANSI half-blocks, 3 tamaños).
- **Bilingüe ES/EN** con persistencia (`phi lang`).
- **`phi doctor`**: comprueba Python, pip, git, pkg y dependencias.
- **Landing page** (GitHub Pages): <https://sebastianl1.github.io/phistack/> con todas las herramientas listadas y descripciones (SEO).
- **Seguridad**: sin `curl | bash` ciego; uso autorizado por categoría.

## Instalación / Installation

```bash
yes|pkg update && yes|pkg upgrade
yes|pkg install git
git clone https://github.com/sebastianl1/phistack.git
cd phistack
bash install.sh
```

El comando `phi` queda disponible.

## Uso / Usage

```
phi                          # menú interactivo / interactive menu
phi list [categoria] [--installed] [--status active] [--source vendor]
phi search <termino>
phi info <tool>
phi install <tool> [tool...]
phi remove <tool> [-y]
phi reinstall <tool>
phi run <tool>
phi term list                # presets de terminal
phi term set <preset>        # aplicar preset (properties, colors, font)
phi term banner <style>      # banner de inicio (phi|quotes|tips|minimal)
phi term prompt <style>      # prompt de fish (phi|minimal)
phi term shell <style>       # config de shell (phi|minimal)
phi term save <nombre>       # guardar tu config como preset
phi ide list / install <preset> / edit / backup
phi lang <es|en>
phi doctor
phi update
phi uninstall
```

## Catálogo / Catalog

Fuente de verdad: `catalog/tools.json` (41 herramientas). Origen: `vendor` (código en `lab/tools/`), `pkg` (repositorios de Termux), `pip` (PyPI) o `download` (binario de release). El informe completo de obsolescencia y mejoras está en `docs/ANALISIS_TOOLS.md`.

## Estructura / Structure

```
phistack/
├── phi.py                  # entry point
├── phistack/               # cli, menus, catalog, installer, presets, theme, fractal, lang, doctor, state, paths
├── catalog/tools.json      # catálogo declarativo (41 tools)
├── lab/
│   ├── tools/<id>/         # código vendorizado de cada herramienta (+LICENSE)
│   ├── termux/             # presets de terminal (properties, colors, font) + banners
│   ├── shell/              # presets de shell (fish: config, prompt) + prompts
│   └── ide/                # presets de IDE (nvim-astrovim)
├── docs/                   # landing GitHub Pages (index.html + lang/*.js + og-image)
├── tests/                  # pytest
├── tools/                  # build_lang.py + i18n_*.json
└── .github/workflows/ci.yml · deploy.yml
```

## Licencias / Licenses

- PhiStack (código del repo): MIT.
- Las herramientas vendorizadas en `lab/tools/` conservan su **propia licencia** (GPL/MIT/Apache). Ver `lab/tools/<id>/LICENSE` y `NOTICE.md`.

## Autor / Author

Sebastian Laguna — familia Phi (OsintPhi · TorPhi · Lamdaphi · PhiStack)
