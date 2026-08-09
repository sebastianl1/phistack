#!/data/data/com.termux/files/usr/bin/bash
# Generic PhiStack MOTD: prints a random entry from a data file.
# Entries are separated by a line containing only ";;;"
BANNER_FILE="__BANNER__"
if [ ! -f "${BANNER_FILE}" ]; then
    exit 0
fi

Y='\e[0;33m' C='\e[0;36m' G='\e[0;32m'
M='\e[0;35m' W='\e[1;37m' N='\e[0m'

total=$(grep -c '^;;;$' "${BANNER_FILE}")
total=$((total + 1))
pick=$((RANDOM % total))
entry=$(awk -v n="$pick" 'BEGIN{c=0} /^;;;$/{c++; next} c==n{print} c>n{exit}' "${BANNER_FILE}")

echo ""
if [ "${pick}" -eq 1 ]; then
    echo -e "  ${C}φ ${N}"
else
    echo -e "  ${M}φ ${N}${W}${entry}${N}"
fi
echo ""
