#!/data/data/com.termux/files/usr/bin/bash
#
# PhiStack - Updater
#
PREFIX=${PREFIX:-/data/data/com.termux/files/usr}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "\033[1;36m[*]\033[0m PhiStack - Actualizando..."
git -C "${SCRIPT_DIR}" pull --ff-only origin main
python3 -m pip install --quiet -r "${SCRIPT_DIR}/requirements.txt"

mkdir -p "${PREFIX}/bin"
cat > "${PREFIX}/bin/phi" <<LAUNCHER
#!/data/data/com.termux/files/usr/bin/bash
exec python3 "${SCRIPT_DIR}/phi.py" "\$@"
LAUNCHER
chmod 755 "${PREFIX}/bin/phi"
chmod 755 "${SCRIPT_DIR}/phi.py"

echo -e "\033[1;32m[✓]\033[0m PhiStack actualizado."
