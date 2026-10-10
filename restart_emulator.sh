#!/usr/bin/env bash
set -e

echo "=== Trezor Emulator: sauberer Neustart ==="

echo "--- Alte Prozesse beenden ---"
pkill -9 -f trezor-emu-core 2>/dev/null || true
pkill -9 -f trezor_safe3_remote.py 2>/dev/null || true
sudo pkill -9 -f trezor-emu-core 2>/dev/null || true
sleep 1

echo "--- Alten Storage-Zustand loeschen ---"
rm -f /var/tmp/trezor.flash /var/tmp/trezor.sdcard /var/tmp/trezor.log /var/tmp/trezor.pid /var/tmp/trezor.port

echo "--- Kontrolle: keine Altprozesse mehr aktiv? ---"
ps aux | grep trezor-emu-core | grep -v grep || echo "(keine gefunden - gut)"

echo ""
echo "=== Emulator wird jetzt gestartet ==="
echo "(dieses Terminal bleibt offen - fuer trezorctl/Remote-Tool ein zweites Terminal oeffnen)"
echo ""

cd ~/trezor-firmware/core
source ../.venv/bin/activate
./emu.py
