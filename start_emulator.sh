#!/usr/bin/env bash
set -e

echo ""
echo "=== Emulator wird jetzt gestartet ==="
echo "(dieses Terminal bleibt offen - fuer trezorctl/Remote-Tool ein zweites Terminal oeffnen)"
echo ""

cd ~/trezor-firmware/core
source ../.venv/bin/activate
./emu.py
