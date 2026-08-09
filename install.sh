#!/data/data/com.termux/files/usr/bin/bash
#
# PhiStack - Installer
# System: Termux (Android)
#
PREFIX=${PREFIX:-/data/data/com.termux/files/usr}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "\n\033[1;36m[*]\033[0m PhiStack - Instalando dependencias..."
yes | pkg install -y python git 2>/dev/null || pkg install -y python git

echo -e "\033[1;36m[*]\033[0m PhiStack - Dependencias de Python..."
python3 -m pip install --quiet -r "${SCRIPT_DIR}/requirements.txt"

echo -e "\033[1;36m[*]\033[0m PhiStack - Creando el comando 'phi'..."
mkdir -p "${PREFIX}/bin"
cat > "${PREFIX}/bin/phi" <<LAUNCHER
#!/data/data/com.termux/files/usr/bin/bash
exec python3 "${SCRIPT_DIR}/phi.py" "\$@"
LAUNCHER
chmod 755 "${PREFIX}/bin/phi"
chmod 755 "${SCRIPT_DIR}/phi.py"

echo -e "\033[1;32m[✓]\033[0m PhiStack instalado. Ejecuta: \033[1;37mphi\033[0m"
