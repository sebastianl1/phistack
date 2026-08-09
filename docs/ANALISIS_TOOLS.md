# Análisis de herramientas: obsoletas vs activas + mejoras

Informe generado a partir de `catalog/tools.json`. Los estados se evaluaron según mantenimiento del proyecto upstream, actividad de releases y funcionalidad conocida (agosto 2026).

| Estado | Cantidad |
|---|---|
| active | 39 |
| legacy | 17 |
| obsolete | 12 |
| api | 3 |
| local | 1 |

## 🟢 Activas (mantenidas y recomendadas)

| Tool | Categoría | Nota | Reemplazo |
|---|---|---|---|
| Sherlock (`sherlock`) | osint | Very active, great for people OSINT. | — |
| theHarvester (`theharvester`) | osint | Modern replacement for Infoga. Official Termux package. | infoga |
| Holehe (`holehe`) | osint | Active and lightweight. Requires network. | — |
| h8mail (`h8mail`) | osint | Active; the successor h8mail2 is better maintained. | h8mail2 |
| h8mail2 (`h8mail2`) | osint |  | — |
| Nexfil (`nexfil`) | osint | Active (thewhiteh4t). | — |
| Octosuite (`octosuite`) | osint | Active (Bellingcat). | — |
| Mosint (`mosint`) | osint | Active. | — |
| PhoneInfoga (`phoneinfoga`) | osint | Active; Go binary from releases. | — |
| ProtoSINT (`protosint`) | osint | Active. | — |
| MagmaOSINT (`magmaosint`) | osint | Active (thewhiteh4t). | — |
| PwnedOrNot (`pwnedornot`) | osint | Active. | — |
| Instaloader (`instaloader`) | osint | Modern successor to SigIT. | sigit |
| Subfinder (`subfinder`) | osint | Recommended replacement for sublist3r. | sublist3r |
| Nmap (`nmap`) | scan | Includes ncat and NSE. Adds vulscan and nmap-vulners. | — |
| Gobuster (`gobuster`) | scan | Active and fast. | — |
| FFUF (`ffuf`) | scan | Modern replacement for dirb. | dirb |
| Nikto (`nikto`) | scan | Active (v2.5.0+). | — |
| WhatWeb (`whatweb`) | scan | Active. | — |
| Sublist3r (`sublist3r`) | scan | Works but slow; subfinder is faster. | subfinder |
| Arjun (`arjun`) | scan | Active. | — |
| httpx (`httpx`) | scan | Modern replacement for Aquatone. | aquatone |
| Nuclei (`nuclei`) | scan | Very active; rapidly growing template base. | — |
| SQLMap (`sqlmap`) | web | Very active; the de facto standard. | — |
| XSS Strike (`xsstrike`) | web | Active. | — |
| Photon (`photon`) | web | Active (s0md3v). | — |
| BeEF (`beef-xss`) | web | Active (v0.5+). For authorized pentests. | — |
| Zphisher (`zphisher`) | phishing | Active. Authorized use only. | weeman |
| Seeker (`seeker`) | phishing | Active (thewhiteh4t). Authorized use only. | — |
| GoPhish (`gophish`) | phishing | Active. For authorized simulations. | — |
| Metasploit (`metasploit`) | exploit | Active; Termux community repo. Heavy install. | — |
| Hydra (`hydra`) | crack | Active; the standard for online brute force. | — |
| John the Ripper (`john`) | crack | Active. | — |
| HashID (`hash-id`) | crack | Active. | — |
| ExifTool (`exiftool`) | forense | De facto forensics standard. | — |
| APKTool (`apktool`) | forense | Active. | — |
| Tmate (`tmate`) | utils | Active. | — |
| Speedtest-cli (`speedtest`) | utils | Works; Ookla speedtest is more accurate. | speedtest-ookla |
| Ookla Speedtest (`speedtest-ookla`) | utils | Recommended replacement for speedtest-cli. | speedtest |

## 🟡 Legacy (funcionales, sin mantenimiento)

| Tool | Categoría | Nota | Reemplazo |
|---|---|---|---|
| ReconDog (`recondog`) | osint | No clear maintenance; partially functional. | — |
| IPHunter (`iphunter`) | osint | Obscure and barely maintained. | — |
| Email2PN (`email2pn`) | osint | Obscure; limited results. | — |
| Wortex (`wortex`) | osint | Obscure. | — |
| Phone-Dox (`phone-dox`) | osint | Obscure; consider phoneinfoga. | phoneinfoga |
| Dirb (`dirb`) | scan | Works but slow; use gobuster or ffuf. | gobuster, ffuf |
| SlowLoris (`slowloris`) | web | Old but simple. Authorized tests only. Alternative: hping3. | hping3 |
| Transwer (`transwer`) | phishing | Obscure. | — |
| Crunch (`crunch`) | crack | Old but functional. | — |
| CUPP (`cupp`) | crack | Works; useful for authorized social engineering. | — |
| Hash-Buster (`hash-buster`) | crack | Old. Use john/hashcat for real cracking. | john, hashcat |
| HashCrypt (`hashcrypt`) | crack | Obscure. | — |
| Netcat (`netcat`) | wireless | Old; ncat (included with nmap) improves on it. | ncat |
| NCShare (`ncshare`) | wireless | Obscure. | — |
| Metagoofil (`metagoofil`) | forense | Original archived; use the v2 version from opsdisk. | exiftool |
| Translate (`translate`) | utils | Obscure. | — |
| QRLink (`qrlink`) | utils | Obscure. | — |

## 🔴 Obsoletas (archivadas/rotas → usar reemplazo)

| Tool | Categoría | Nota | Reemplazo |
|---|---|---|---|
| Infoga (`infoga`) | osint | Archived since 2021. Use theHarvester. | theharvester |
| SigIT (`sigit`) | osint | Broken by Instagram API changes. Avoid third-party accounts. | instaloader |
| FBUserID (`fbuserid`) | osint | Broken by Facebook changes; unmaintained. | none |
| OnionSearch (`onionsearch`) | osint | Archived; consider TorPhi (your project) for Tor browsing. | torphi |
| Aquatone (`aquatone`) | scan | Project archived (2021). Use httpx + screenshots. | httpx, eyewitness |
| RedHawk (`redhawk`) | scan | Archived. Use nmap + whatweb + nuclei. | nmap, whatweb, nuclei |
| Weeman (`weeman`) | phishing | Abandoned. Use zphisher or your Lamdaphi. | zphisher, lamdaphi |
| SayCheese (`saycheese`) | phishing | From thelinuxchoice author (archived). High ethical risk. | seeker |
| EvilURL (`evilurl`) | phishing | From thelinuxchoice author (archived). | none |
| Ghost (`ghost`) | phishing | Archived (entynetproject). | gophish, beef-xss |
| Routersploit (`routersploit`) | exploit | Archived (2022). Use Metasploit auxiliary modules. | metasploit |
| PhoneSploit (`phonesploit`) | exploit | Archived (entynetproject). Modern ADB partially replaces it. | adb |

## 🟣 Requieren API

| Tool | Categoría | Nota | Reemplazo |
|---|---|---|---|
| Shodan CLI (`shodan`) | utils | Requires SHODAN_API_KEY. | — |
| VirusTotal CLI (`virustotal`) | utils | Requires VT_API_KEY. | — |
| ChatGPT CLI (`chatgpt`) | utils | Depends on OpenAI API; consider randi (local AI). | randi |

## 🔵 Local/Regional

| Tool | Categoría | Nota | Reemplazo |
|---|---|---|---|
| Ecuador-ID (`ecuador-id`) | osint | Regional tool (Ecuador). | — |


## Mejoras sugeridas (ya implementadas en el catálogo)

1. **Aquatone → httpx**: Aquatone está archivado (2021). `httpx` (projectdiscovery) hace probing, fingerprinting y screenshots, y sigue activo.
2. **Infoga → theHarvester**: Infoga archivado (2021). `theHarvester` es el estándar moderno y está en el repo de Termux.
3. **Dirb → ffuf / gobuster**: Dirb funciona pero es lento. `ffuf` es un fuzzer moderno y rápido.
4. **Sublist3r → subfinder**: Sublist3r sigue activo pero es lento. `subfinder` es más rápido y activo.
5. **Sigit → instaloader**: SigIT roto por API de Instagram. `instaloader` está mantenido.
6. **Weeman → zphisher**: Weeman abandonado. `zphisher` es el kit de phishing más usado y activo.
7. **OnionSearch → TorPhi (tu proyecto)**: archivado; tu TorPhi lo cubre con mejor UX.
8. **Routersploit → Metasploit auxiliares**: archivado (2022).
9. **RedHawk → nmap + whatweb + nuclei**: archivado.
10. **Hash-Buster → john / hashcat**: online-only y viejo.
11. **h8mail → h8mail2**: h8mail2 está más mantenido (ambos disponibles).
12. **Netcat → ncat**: ncat (incluido con nmap) mejora netcat clásico.
13. **Speedtest-cli → speedtest-go (Ookla)**: más preciso.
14. **ChatGPT CLI → randi (tu proyecto)**: el CLI depende de la API de OpenAI; randi corre LLMs locales.

## Mejoras arquitectónicas de PhiStack

- **Catálogo declarativo JSON** en lugar de cadenas de `if/elif` (~230 líneas de dispatch).
- **Estado idempotente** (`~/.phistack/state.json`): reinstalar no rompe.
- **Verificación real** tras instalar (`verify`), no solo copiar binarios.
- **Shebang corregido** para Termux en todos los launchers.
- **Auditoría supply-chain**: soporte `sha256` en descargas; sin `curl | bash` ciego.
- **Bilingüe** ES/EN con selector persistente.
- **Menús interactivos** profesionales (InquirerPy) en modo interactivo.
- **`phi doctor`** para diagnosticar el entorno antes de instalar.
- **CI + tests** para no romper el catálogo al añadir herramientas.

## Herramientas que se descartaron de la migración

- **Aquatone**: sustituida por `httpx`.
- **Nada más se eliminó**: el resto se conserva marcando su estado real.
