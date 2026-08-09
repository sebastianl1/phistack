# Análisis de herramientas: catálogo curado v2

PhiStack v2 mantiene solo herramientas **funcionales y auditadas**. Las
herramientas de script se **vendorizan** en `lab/tools/<id>/` (código dentro del
repositorio, sin depender de `git clone` de terceros); las compiladas se
instalan vía `pkg`; las de PyPI vía `pip`; y los binarios vía release oficial.

## Catálogo (41 herramientas)

| Categoría | Herramientas | Fuente |
|---|---|---|
| OSINT | sherlock, theHarvester, holehe, h8mail, nexfil, ProtoSINT, PwnedOrNot, Octosuite, PhoneInfoga, Instaloader, Subfinder | vendor / pkg / pip / download |
| Escaneo | nmap, gobuster, ffuf, nikto, whatweb, sublist3r, arjun, nuclei | pkg / pip |
| Web | sqlmap, XSStrike, Photon, SlowLoris | vendor |
| Explotación | metasploit | pkg |
| Contraseñas | hydra, john, hashcat, crunch, cupp, HashID | pkg / vendor |
| Phishing | zphisher, Seeker, GoPhish | vendor / download |
| Red | netcat | pkg |
| Forense | exiftool, Metagoofil, APKTool | pkg / vendor |
| Utilidades | tmate, speedtest-cli, Shodan (API), VirusTotal CLI (API) | pkg / pip |

**Vendorizadas (15)**: sqlmap, sherlock, xsstrike, photon, cupp, hash-id, nexfil,
metagoofil, zphisher, seeker, holehe, h8mail, protosint, pwnedornot, slowloris.

## Eliminadas en v2

Las siguientes herramientas fueron eliminadas por **obsoletas, archivadas o
insalvables** (no fue posible hacerlas funcionales o vendorizarlas):

| Herramienta | Motivo |
|---|---|
| aquatone | Proyecto archivado (2021) |
| infoga | Archivado (2021); reemplazado por theHarvester |
| redhawk | Archivado |
| routersploit | Archivado (2022) |
| weeman | Abandonado; reemplazado por zphisher |
| sigit | Roto por API de Instagram |
| fbuserid | Roto por cambios de Facebook |
| onionsearch | Archivado; TorPhi lo cubre |
| saycheese | Archivado; riesgo ético alto |
| evilurl | Archivado |
| ghost | Archivado |
| phonesploit | Archivado |
| mosint | Herramienta Go (no vendorizable como script) |
| magmaosint | Repositorio eliminado (no disponible) |
| octosuite (vendored) | Revertido a pip (distribución oficial) |
| iphunter, email2pn, wortex, phone-dox, ncshare, transwer, translate, qrlink, hash-buster, hashcrypt, recondog, ecuador-id, beef-xss, chatgpt, h8mail2, httpx, speedtest-ookla | Obscuras, rotas o sin valor claro para el laboratorio |

## Licencias

Cada herramienta vendorizada conserva su propia licencia (`lab/tools/<id>/LICENSE`).
El MIT de PhiStack aplica solo al código del propio proyecto. Ver `NOTICE.md`.

## Mejoras arquitectónicas de PhiStack

- **Vendoring**: el código de las herramientas vive dentro del repo → instalación
  reproducible sin red y sin depender del estado de repositorios de terceros.
- **Catálogo declarativo JSON** con `source` (vendor/pkg/pip/download) y `verify`.
- **Motor idempotente**: copia local + deps + launcher + verificación real.
- **Laboratorio**: presets de terminal e IDE capturados, con variaciones y guardado.
- **Menús interactivos** (InquirerPy) y listado agrupado por categoría con `rich`.
