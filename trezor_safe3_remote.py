#!/usr/bin/env python3
"""
Virtuelles Bedienfeld fuer den Trezor Safe 3 (T2B1) Emulator.

Bildet die zwei physischen Tasten (links/rechts) sowie die
Bestaetigungsgesten (Mitte/Ja/Nein) als grosse, per Kopfmaus
anklickbare Buttons ab und sendet sie ueber DebugLink an den
laufenden Emulator (udp:127.0.0.1:21324).

Voraussetzung: der Emulator (`./emu.py`) muss bereits laufen.
"""
import tkinter as tk
from trezorlib.transport import get_transport
from trezorlib.debuglink import DebugLink

TRANSPORT_PATH = "udp:127.0.0.1:21325"


def main():
    transport = get_transport(TRANSPORT_PATH)
    debuglink = DebugLink(transport)
    debuglink.open()

    root = tk.Tk()
    root.title("Trezor Safe 3 - Virtuelles Bedienfeld")
    root.geometry("420x360")

    status_var = tk.StringVar(value="Bereit.")

    def show_layout():
        try:
            layout = debuglink.read_layout()
            status_var.set(str(layout)[:200])
        except Exception as e:
            status_var.set(f"Fehler beim Lesen: {e}")

    def do(action_name, fn):
        def handler():
            try:
                fn()
                status_var.set(f"Aktion gesendet: {action_name}")
                root.after(150, show_layout)
            except Exception as e:
                status_var.set(f"Fehler bei '{action_name}': {e}")
        return handler

    button_specs = [
        ("\u25c0  Links (scroll)", do("press_left", debuglink.press_left)),
        ("\u25b6  Rechts (scroll)", do("press_right", debuglink.press_right)),
        ("\u25cf  Mitte (auswaehlen)", do("press_middle", debuglink.press_middle)),
        ("\u2714  Bestaetigen (Ja)", do("press_yes", debuglink.press_yes)),
        ("\u2714\u2714  Bestaetigen (Ja, HALTEN 1.5s)", do("press_yes_hold", lambda: debuglink.press_yes(hold_ms=1500))),
        ("\u2716  Abbrechen (Nein)", do("press_no", debuglink.press_no)),
        ("\u21bb  Bildschirm aktualisieren", show_layout),
    ]

    for label, cmd in button_specs:
        b = tk.Button(root, text=label, font=("Sans", 16), height=2, command=cmd)
        b.pack(fill="x", padx=12, pady=6)

    status_label = tk.Label(root, textvariable=status_var, wraplength=380,
                             justify="left", font=("Sans", 10))
    status_label.pack(fill="x", padx=12, pady=10)

    show_layout()
    root.mainloop()
    debuglink.close()


if __name__ == "__main__":
    main()
