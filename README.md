# PhiStack 🐍

Gestor de stack para Termux, bilingüe (ES/EN), con menús interactivos estilo InquirerPy.

Stack manager for Termux, bilingual (ES/EN), with InquirerPy-style interactive menus.

> Uso autorizado únicamente. Muchas herramientas son para pruebas de seguridad.
> No pruebes sistemas que no te pertenecen o sin permiso explícito.
>
> Authorized use only. Many tools are for security testing.
> Do not test systems you do not own or without explicit permission.

## Características / Features

- **72 herramientas** categorizadas y analizadas (activas / legacy / obsoletas / API).
- **Catálogo declarativo** en JSON (`catalog/tools.json`) — sin monstruos de `if/elif`.
- **Menús interactivos** con [InquirerPy](https://github.com/kazhala/InquirerPy): select, fuzzy, checkbox, confirm.
- **Modo interactivo y CLI**: `phi` abre el menú; `phi install <tool>` por línea de comandos.
- **Bilingüe ES/EN** con persistencia (`phi lang`).
- **Análisis de obsolescencia** por herramienta: marca obsoletas y sugiere reemplazos modernos.
- **Doctor**: comprueba Python, pip, git, pkg y dependencias.
- **Banner fractal**: conjunto de Mandelbrot renderizado en ANSI truecolor con half-blocks, paleta duotono azul y 3 tamaños.
- **Estilo Termux** propio: banner, prompt de fish y tema de colores.
- **Landing page** (GitHub Pages): <https://sebastianl1.github.io/phistack/> (6 idiomas, SEO + JSON-LD + llms.txt).
- **Seguridad**: SHA256 para descargas directas, sin `curl | bash` ciego.

## Instalación / Installation

```bash
yes|pkg update && yes|pkg upgrade
yes|pkg install git
git clone https://github.com/<tu-usuario>/phistack.git
cd phistack
bash install.sh
```

El comando `phi` queda disponible.

The `phi` command becomes available.

## Uso / Usage

```
phi                          # menú interactivo / interactive menu
phi help
phi list [categoria]         # listar / list
phi list --status obsolete
phi search <termino>
phi info <tool>
phi install <tool> [tool...]
phi remove <tool> [-y]
phi reinstall <tool>
phi run <tool>
phi theme                    # banner / prompt
phi lang <es|en>
phi doctor
phi update
phi uninstall
```

### Categorías / Categories

`osint` · `scan` · `web` · `exploit` · `crack` · `phishing` · `wireless` · `forense` · `utils`

## Estado de herramientas / Tool status

| Estado | Significado |
|---|---|
| 🟢 active | Mantenida y recomendada / Maintained and recommended |
| 🟡 legacy | Funcional pero sin mantenimiento / Functional, unmaintained |
| 🔴 obsolete | Archivada/rota, usa el reemplazo / Archived/broken, use replacement |
| 🟣 api | Requiere API key / Requires API key |
| 🔵 local | Regional/personal / Regional/personal |

Consulta `docs/ANALISIS_TOOLS.md` para el informe completo de obsolescencia y mejoras.

## Estructura / Structure

```
phistack/
├── phi.py                  # entry point
├── phistack/
│   ├── cli.py              # subcomandos + modo interactivo
│   ├── fractal.py          # banner: Mandelbrot + espiral áurea (ANSI half-block + PNG)
│   ├── menus.py            # wrappers InquirerPy
│   ├── catalog.py          # carga/valida tools.json
│   ├── installer.py        # motor pkg/git/pip/run/download/launcher
│   ├── state.py            # estado de instalación (.phistack/state.json)
│   ├── style.py            # banner, prompt, tema
│   ├── lang.py             # ES/EN
│   ├── doctor.py           # diagnóstico
│   └── paths.py            # rutas (Termux-aware)
├── catalog/tools.json      # catálogo declarativo (72 tools)
├── style/                  # prompt fish, termux.properties, colors
├── tools/                  # build_lang.py + i18n_*.json (generan docs/lang)
├── tests/                  # pytest
├── docs/                   # landing GitHub Pages (index.html + lang/*.js + og-image)
│   ├── lang/{es,en,pt,fr,de,zh}.js
│   └── ANALISIS_TOOLS.md   # informe de obsolescencia
├── install.sh / update.sh / uninstall.sh
└── .github/workflows/ci.yml · deploy.yml
```

## Desarrollo / Development

```bash
python3 -m pytest tests/ -q     # tests
python3 phi.py --banner         # probar banner
python3 phi.py list             # probar CLI sin instalar
```

## Autor / Author

Sebastian Laguna — familia Phi (OsintPhi · TorPhi · Lamdaphi · PhiStack)

## Licencia / License

MIT
