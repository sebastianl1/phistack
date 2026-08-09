# Changelog

Todas las notas de versiones de PhiStack. Sigue [Keep a Changelog](https://keepachangelog.com/) y [SemVer](https://semver.org/).

## [2.0.0] - 2026-08-09

### Added
- **Concepto "Laboratorio Termux"**: PhiStack ahora estructura el terminal completo (dev + ciberseguridad), no solo instala herramientas.
- **`phi term`** (Laboratorio de terminal): presets de banner de inicio, prompt de fish, colores y fuente; variaciones (banner phi/quotes/tips/minimal, prompt phi/minimal, shell phi/minimal); `list|set|banner|prompt|shell|save|edit`.
- **`phi ide`** (Laboratorio de IDE): preset `nvim-astrovim` (config real del autor vendorizada) + `list|install|edit|backup`.
- **Catálogo curado (41 herramientas)**: auditoría tool por tool; se eliminaron las obsoletas/rotas (aquatone, infoga, routersploit, weeman, sigit, fbuserid, onionsearch, saycheese, evilurl, ghost, phonesploit, redhawk, mosint, magmaosint y otras oscuras).
- **Vendoring**: 15 herramientas de script vendorizadas en `lab/tools/<id>/` con su LICENSE; el motor de instalación las copia localmente (sin `git clone` de terceros). Se añadió `hashcat`.
- **`NOTICE.md`** con las licencias de cada herramienta vendorizada.
- **Banner del conjunto de Mandelbrot completo** en silueta 2 tonos (reemplaza el zoom previo).
- **Presentación**: `phi list` agrupa por categoría con estado, fuente e indicador de instalada; filtros `--status`, `--installed`, `--source`, `--detail`.
- **Menú interactivo por secciones** (Laboratorio / Herramientas / Sistema).
- **Landing v2**: todas las herramientas listadas con descripción como HTML estático (SEO), sección "Laboratorio", i18n ampliado (117 claves x6).

### Changed
- `catalog/tools.json`: versión 2.0, campo `source` (vendor/pkg/pip/download).
- Banner: ahora es el conjunto de Mandelbrot completo en silueta 2 tonos.

### Removed
- Herramientas obsoletas, rotas o no vendorizables (ver análisis en `docs/ANALISIS_TOOLS.md`).

## [1.0.0] - 2026-08-08

### Added
- Catálogo inicial de 72 herramientas con análisis de obsolescencia.
- Reemplazos modernos añadidos: theHarvester (infoga), subfinder (sublist3r), ffuf (dirb), httpx (aquatone), nuclei, zphisher (weeman), instaloader (sigit), h8mail2 (h8mail), speedtest-ookla (speedtest-cli).
- CLI `phi` con subcomandos: list, search, info, install, remove, reinstall, run, lang, theme, doctor, update, uninstall.
- Modo interactivo con menús InquirerPy (select / fuzzy / checkbox / confirm).
- Sistema bilingüe ES/EN persistente.
- Motor de instalación declarativo: pkg / git / pip / run / download / launcher con verificación y estado idempotente.
- `phi doctor`: chequeo de Python, pip, git, pkg y dependencias.
- **Banner fractal**: conjunto de Mandelbrot renderizado en ANSI truecolor con half-blocks, paleta duotono azul (small/medium/large).
- **Landing page** GitHub Pages: `docs/` con el mismo diseño de landing que el resto de proyectos del autor (6 idiomas, JSON-LD, OG/Twitter, robots, sitemap, llms.txt, og-image generada con el fractal).
- Workflow `.github/workflows/deploy.yml` para GitHub Pages.
- Tests pytest (17) y CI en GitHub Actions (Python 3.11-3.13).

### Changed
- Arquitectura de cadenas if/elif → catálogo JSON declarativo.
- Banners, prompt y tema totalmente nuevos: el banner ahora es un fractal del conjunto de Mandelbrot (sin texto), no los banners figlet con el nombre.

### Fixed
- Referencias rotas de instaladores heredados eliminadas por diseño declarativo.
- Shebang de launchers corregido para Termux (`#!$PREFIX/bin/bash`).
- Bug de colisión del parámetro `lang` en `t()` resuelto.
- Destino `opt` de los clones `git` ahora resuelve a `$PREFIX/opt` (antes creaba `opt/` relativo al CWD).
- `phi remove` detecta binarios instalados aunque no estén en el estado; `-y/--yes` permite no interactivo.
- `phi doctor` corregido al validar requisitos con strings.
- Menús InquirerPy usan el estilo por defecto (compatible con prompt_toolkit>=3.0.53).
