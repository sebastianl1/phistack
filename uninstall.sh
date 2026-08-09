#!/data/data/com.termux/files/usr/bin/bash
#
# PhiStack - Uninstaller
#
PREFIX=${PREFIX:-/data/data/com.termux/files/usr}

echo -e "\033[1;36m[*]\033[0m PhiStack - Eliminando comando 'phi'..."
rm -f "${PREFIX}/bin/phi"

echo -e "\033[1;36m[*]\033[0m PhiStack - Eliminando configuración..."
rm -rf "${HOME}/.phistack"

echo -e "\033[1;32m[✓]\033[0m PhiStack desinstalado. Elimina la carpeta del repo manualmente."
