#!/bin/bash
# start.sh — Lance le dashboard système Parrot OS

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ╔═══════════════════════════════╗"
echo "  ║   PARROT // SYS DASHBOARD    ║"
echo "  ╚═══════════════════════════════╝"
echo -e "${NC}"

# Vérifier Python3
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 requis. Instale li: sudo apt install python3"
    exit 1
fi

# Installer dépendances si absent
echo -e "${GREEN}[✔]${NC} Verifikasyon depandans..."
pip3 install flask flask-cors psutil --break-system-packages -q 2>/dev/null || \
pip3 install flask flask-cors psutil -q 2>/dev/null

echo -e "${GREEN}[✔]${NC} Lancement du serveur..."
echo -e "${GREEN}[✔]${NC} Dashboard disponib sou: ${CYAN}http://localhost:5000${NC}"
echo ""
echo "  Ctrl+C pou kanpe"
echo ""

# Ouvrir browser automatiquement (Parrot OS)
sleep 1 && xdg-open http://localhost:5000 2>/dev/null &

python3 server.py
