#!/usr/bin/env python3
"""Arc Raider Material Tracker - Squad coordination tool with Discord webhook integration."""

import json
import os
import threading
import tkinter as tk
import requests
from tkinter import ttk, messagebox
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATERIALS_FILE = os.path.join(BASE_DIR, "materials.json")
PLAYER_DATA_FILE = os.path.join(BASE_DIR, "player_data.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_MATERIALS = [
    # A
    "Advanced ARC Powercell",
    "Advanced Electrical Components",
    "Advanced Mechanical Components",
    "Agave",
    "Agave Juice",
    "Air Freshener",
    "Alarm Clock",
    "Antiseptic",
    "Apricot",
    "ARC Alloy",
    "ARC Circuitry",
    "ARC Coolant",
    "ARC Flex Rubber",
    "ARC Motion Core",
    "ARC Performance Steel",
    "ARC Powercell",
    "ARC Synthetic Resin",
    "ARC Thermo Lining",
    "Assorted Seeds",
    # B
    "Bastion Cell",
    "Battery",
    "Bicycle Pump",
    "Bloated Tuna Can",
    "Bombardier Cell",
    "Breathtaking Snow Globe",
    "Broken Flashlight",
    "Broken Guidance System",
    "Broken Handheld Radio",
    "Broken Taser",
    "Burned ARC Circuitry",
    # C
    "Camera Lens",
    "Candleberries",
    "Candle Holder",
    "Canister",
    "Cat Bed",
    "Chemicals",
    "Coffee Pot",
    "Complex Gun Parts",
    "Coolant",
    "Cooling Coil",
    "Cooling Fan",
    "Cracked Bioscanner",
    "Crude Explosives",
    "Crumpled Plastic Bottle",
    # D
    "Damaged ARC Motion Core",
    "Damaged ARC Powercell",
    "Damaged Fireball Burner",
    "Damaged Heat Sink",
    "Damaged Hornet Driver",
    "Damaged Rocketeer Driver",
    "Damaged Tick Pod",
    "Damaged Wasp Driver",
    "Dart Board",
    "Deflated Football",
    "Degraded ARC Rubber",
    "Diving Goggles",
    "Dog Collar",
    "Dried-Out ARC Resin",
    "Duct Tape",
    "Durable Cloth",
    # E
    "Electrical Components",
    "Empty Wine Bottle",
    "Exodus Modules",
    "Expired Pasta",
    "Expired Respirator",
    "Explosive Compound",
    # F
    "Fabric",
    "Faded Photograph",
    "Fertilizer",
    "Film Reel",
    "Fine Wristwatch",
    "Fireball Burner",
    "Flow Controller",
    "Fossilized Lightning",
    "Frequency Modulation Box",
    "Fried Motherboard",
    "Frying Pan",
    # G
    "Garlic Press",
    "Geiger Counter",
    "Great Mullein",
    # H
    "Headphones",
    "Heavy Gun Parts",
    "Hornet Driver",
    "Household Cleaner",
    "Humidifier",
    # I
    "Ice Cream Scooper",
    "Impure ARC Coolant",
    "Industrial Battery",
    "Industrial Charger",
    "Industrial Magnet",
    "Ion Sputter",
    # L
    "Laboratory Reagents",
    "Lance's Mixtape (5th Edition)",
    "Leaper Pulse Unit",
    "Lemon",
    "Light Bulb",
    "Light Gun Parts",
    # M
    "Magnet",
    "Magnetic Accelerator",
    "Magnetron",
    "Matriarch Reactor",
    "Mechanical Components",
    "Medium Gun Parts",
    "Metal Brackets",
    "Metal Parts",
    "Microscope",
    "Mini Centrifuge",
    "Mod Components",
    "Moss",
    "Motor",
    "Mushroom",
    "Music Album",
    "Music Box",
    # N
    "Number Plate",
    # O
    "Oil",
    "Olives",
    # P
    "Painted Box",
    "Plastic Parts",
    "Playing Cards",
    "Polluted Air Filter",
    "Pop Trigger",
    "Portable TV",
    "Poster of Natural Wonders",
    "Pottery",
    "Power Bank",
    "Power Cable",
    "Power Rod",
    "Prickly Pear",
    "Processor",
    # Q
    "Queen Reactor",
    # R
    "Radio",
    "Radio Relay",
    "Recorder",
    "Red Coral Jewelry",
    "Remote Control",
    "Resin",
    "Ripped Safety Vest",
    "Rocket Thruster",
    "Rocketeer Driver",
    "Roots",
    "Rope",
    "Rosary",
    "Rotary Encoder",
    "Rubber Duck",
    "Rubber Pad",
    "Rubber Parts",
    "Ruined Accordion",
    "Ruined Baton",
    "Ruined Handcuffs",
    "Ruined Parachute",
    "Ruined Riot Shield",
    "Ruined Tactical Vest",
    "Rusted Bolts",
    "Rusted Gear",
    "Rusted Shut Medical Kit",
    "Rusted Tools",
    "Rusty ARC Steel",
    # S
    "Sample Cleaner",
    "Sensors",
    "Sentinel Firing Core",
    "Shredder Gyro",
    "Signal Amplifier",
    "Silver Teaspoon Set",
    "Simple Gun Parts",
    "Snitch Scanner",
    "Speaker Component",
    "Spectrometer",
    "Spectrum Analyzer",
    "Spotter Relay",
    "Spring Cushion",
    "Statuette",
    "Steel Spring",
    "Surveyor Vault",
    "Synthesized Fuel",
    "Syringe",
    # T
    "Tattered ARC Lining",
    "Tattered Clothes",
    "Telemetry Transceiver",
    "Thermostat",
    "Tick Pod",
    "Toaster",
    "Torn Book",
    "Torn Blanket",
    "Turbo Pump",
    # U
    "Unusable Weapon",
    # V
    "Vase",
    "Very Comfortable Pillow",
    "Volcanic Rock",
    "Voltage Converter",
    # W
    "Wasp Driver",
    "Water Filter",
    "Water Pump",
    "Wires",
]

DISCORD_COLORS = {
    "needs": 0xE74C3C,   # red
    "have":  0x2ECC71,   # green
    "both":  0x3498DB,   # blue
}


class ScrollableFrame(ttk.Frame):
    """A frame that scrolls vertically inside a canvas."""

    def __init__(self, parent, **kwargs):
        self.canvas = tk.Canvas(parent, highlightthickness=0, **kwargs)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        super().__init__(self.canvas)

        self._window = self.canvas.create_window((0, 0), window=self, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mousewheel bindings (cross-platform)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _on_frame_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self._window, width=event.width)

    def _bind_mousewheel(self, _event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def pack_canvas(self, **kwargs):
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(**kwargs)


class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, config_data, on_save, on_test):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("540x160")
        self.resizable(False, False)
        self.grab_set()
        self.on_save = on_save
        self.on_test = on_test

        ttk.Label(self, text="Discord Webhook URL:").grid(row=0, column=0, padx=12, pady=14, sticky="w")
        self.webhook_var = tk.StringVar(value=config_data.get("webhook_url", ""))
        ttk.Entry(self, textvariable=self.webhook_var, width=52).grid(row=0, column=1, columnspan=2, padx=5, pady=14)

        ttk.Label(self, text="(Paste the webhook URL from your Discord channel settings.)",
                  foreground="gray").grid(row=1, column=0, columnspan=3, padx=12, sticky="w")

        self.status_var = tk.StringVar()
        ttk.Label(self, textvariable=self.status_var, foreground="gray").grid(
            row=2, column=0, columnspan=3, padx=12, sticky="w")

        ttk.Button(self, text="Test", command=self._test).grid(row=3, column=0, padx=12, pady=8, sticky="w")
        ttk.Button(self, text="Save", command=self._save).grid(row=3, column=2, padx=12, pady=8, sticky="e")
        ttk.Button(self, text="Cancel", command=self.destroy).grid(row=3, column=1, pady=8, sticky="e")

    def _test(self):
        url = self.webhook_var.get().strip()
        if not url:
            self.status_var.set("Enter a webhook URL first.")
            return
        self.status_var.set("Sending test message…")
        self.on_test(url, self._on_test_result)

    def _on_test_result(self, ok: bool, detail: str):
        self.status_var.set("✅ Test message sent!" if ok else f"❌ {detail}")

    def _save(self):
        self.on_save(self.webhook_var.get().strip())
        self.destroy()


class MaterialsManagerDialog(tk.Toplevel):
    def __init__(self, parent, materials, on_save):
        super().__init__(parent)
        self.title("Manage Materials")
        self.geometry("360x520")
        self.grab_set()
        self.on_save = on_save

        ttk.Label(self, text="Edit the material list (one per line):").pack(padx=10, pady=(10, 4), anchor="w")
        ttk.Label(self, text="Changes apply after saving and rebuild the tracker.",
                  foreground="gray").pack(padx=10, anchor="w")

        self.text = tk.Text(self, width=42, height=28, font=("Courier", 10))
        self.text.pack(padx=10, pady=6, fill="both", expand=True)
        self.text.insert("1.0", "\n".join(materials))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=8)
        ttk.Button(btn_frame, text="Reset to Defaults", command=self._reset).pack(side="left")
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side="right")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right", padx=4)

    def _reset(self):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "\n".join(DEFAULT_MATERIALS))

    def _save(self):
        lines = [l.strip() for l in self.text.get("1.0", "end").splitlines() if l.strip()]
        if not lines:
            messagebox.showwarning("Empty List", "Material list cannot be empty.", parent=self)
            return
        self.on_save(lines)
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arc Raider Material Tracker")
        self.geometry("760x660")
        self.minsize(640, 480)

        self._config = self._load_json(CONFIG_FILE, {"player_name": "", "webhook_url": ""})
        self.materials = self._load_json(MATERIALS_FILE, DEFAULT_MATERIALS)
        self._player_data = self._load_json(PLAYER_DATA_FILE, {})

        self.need_vars: dict[str, tk.IntVar] = {}
        self.have_vars: dict[str, tk.IntVar] = {}

        self._apply_style()
        self._build_ui()

    # ── Style ──────────────────────────────────────────────────────────────────

    def _apply_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Header.TLabel", font=("", 10, "bold"))
        style.configure("Action.TButton", padding=(8, 4))
        style.configure("Post.TButton", padding=(10, 5))

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top bar ──
        top = ttk.Frame(self, padding=(10, 8))
        top.pack(fill="x")

        ttk.Label(top, text="🎮 Arc Raider Material Tracker", font=("", 13, "bold")).pack(side="left")
        ttk.Button(top, text="⚙ Settings", command=self._open_settings).pack(side="right")
        ttk.Button(top, text="📋 Materials", command=self._open_materials_manager).pack(side="right", padx=6)

        # ── Player name ──
        player_bar = ttk.Frame(self, padding=(10, 0, 10, 6))
        player_bar.pack(fill="x")
        ttk.Label(player_bar, text="Your name:").pack(side="left")
        self.player_name_var = tk.StringVar(value=self._config.get("player_name", ""))
        ttk.Entry(player_bar, textvariable=self.player_name_var, width=22).pack(side="left", padx=6)
        ttk.Label(player_bar, text="(shown in Discord posts)", foreground="gray").pack(side="left")

        ttk.Separator(self).pack(fill="x")

        # ── Scrollable material table ──
        table_outer = ttk.Frame(self, padding=6)
        table_outer.pack(fill="both", expand=True)

        self.sf = ScrollableFrame(table_outer, bg="#f4f4f4")
        self._build_table_header()
        self.sf.pack_canvas(side="left", fill="both", expand=True)

        self._build_material_rows()

        ttk.Separator(self).pack(fill="x")

        # ── Action buttons ──
        btn_bar = ttk.Frame(self, padding=(10, 8))
        btn_bar.pack(fill="x")

        ttk.Button(btn_bar, text="Save", command=self._save_data, style="Action.TButton").pack(side="left")
        ttk.Button(btn_bar, text="Clear All", command=self._clear_all, style="Action.TButton").pack(side="left", padx=6)

        ttk.Button(btn_bar, text="📤 Post All", command=lambda: self._post("both"),
                   style="Post.TButton").pack(side="right")
        ttk.Button(btn_bar, text="🟢 Post Offers", command=lambda: self._post("have"),
                   style="Post.TButton").pack(side="right", padx=6)
        ttk.Button(btn_bar, text="🔴 Post Needs", command=lambda: self._post("needs"),
                   style="Post.TButton").pack(side="right")

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready — fill in quantities, then post to Discord.")
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w",
                  padding=(6, 3)).pack(fill="x", side="bottom")

    def _build_table_header(self):
        f = self.sf
        ttk.Label(f, text="Material", style="Header.TLabel", width=28).grid(
            row=0, column=0, padx=(6, 2), pady=4, sticky="w")
        ttk.Label(f, text="I Need", style="Header.TLabel", width=10, anchor="center").grid(
            row=0, column=1, padx=4, pady=4)
        ttk.Label(f, text="I Have to Share", style="Header.TLabel", width=15, anchor="center").grid(
            row=0, column=2, padx=4, pady=4)
        ttk.Separator(f, orient="horizontal").grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=2)

    def _build_material_rows(self):
        # Remove old rows (keep header rows 0 and 1)
        for widget in self.sf.winfo_children():
            info = widget.grid_info()
            if info and int(info.get("row", 0)) >= 2:
                widget.destroy()

        self.need_vars.clear()
        self.have_vars.clear()

        for i, material in enumerate(self.materials):
            row = i + 2
            saved = self._player_data.get(material, {})

            need_var = tk.IntVar(value=saved.get("need", 0))
            have_var = tk.IntVar(value=saved.get("have", 0))
            self.need_vars[material] = need_var
            self.have_vars[material] = have_var

            bg = "#f0f0f0" if i % 2 == 0 else "#ffffff"
            lbl = tk.Label(self.sf, text=material, width=28, anchor="w",
                           bg=bg, font=("", 10), pady=2)
            lbl.grid(row=row, column=0, padx=(6, 2), pady=1, sticky="ew")

            need_spin = ttk.Spinbox(self.sf, from_=0, to=9999, textvariable=need_var,
                                    width=7, justify="center")
            need_spin.grid(row=row, column=1, padx=4, pady=1)

            have_spin = ttk.Spinbox(self.sf, from_=0, to=9999, textvariable=have_var,
                                    width=7, justify="center")
            have_spin.grid(row=row, column=2, padx=4, pady=1)

    # ── Data helpers ───────────────────────────────────────────────────────────

    def _load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return default

    def _save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _save_data(self):
        self._config["player_name"] = self.player_name_var.get().strip()
        self._save_json(CONFIG_FILE, self._config)

        data = {}
        for m in self.materials:
            n, h = self.need_vars[m].get(), self.have_vars[m].get()
            if n > 0 or h > 0:
                data[m] = {"need": n, "have": h}
        self._player_data = data
        self._save_json(PLAYER_DATA_FILE, data)
        self._set_status("Saved.")

    def _clear_all(self):
        for v in self.need_vars.values():
            v.set(0)
        for v in self.have_vars.values():
            v.set(0)
        self._set_status("Cleared.")

    # ── Discord posting ────────────────────────────────────────────────────────

    def _post(self, mode: str):
        webhook_url = self._config.get("webhook_url", "").strip()
        if not webhook_url:
            messagebox.showwarning("No Webhook URL",
                                   "Please add your Discord webhook URL in Settings first.")
            self._open_settings()
            return

        player = self.player_name_var.get().strip() or "A squadmate"

        needs = [(m, self.need_vars[m].get()) for m in self.materials if self.need_vars[m].get() > 0]
        haves = [(m, self.have_vars[m].get()) for m in self.materials if self.have_vars[m].get() > 0]

        if mode == "needs" and not needs:
            messagebox.showinfo("Nothing to Post", "You haven't marked any materials as needed.")
            return
        if mode == "have" and not haves:
            messagebox.showinfo("Nothing to Post", "You haven't marked any materials to share.")
            return
        if mode == "both" and not needs and not haves:
            messagebox.showinfo("Nothing to Post", "Mark some quantities first.")
            return

        embeds = []
        if mode in ("needs", "both") and needs:
            embeds.append({
                "title": f"🔴 {player} needs materials",
                "description": "\n".join(f"• **{m}** × {qty}" for m, qty in needs),
                "color": DISCORD_COLORS["needs"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "footer": {"text": "Arc Raider Material Tracker"},
            })
        if mode in ("have", "both") and haves:
            embeds.append({
                "title": f"🟢 {player} can share materials",
                "description": "\n".join(f"• **{m}** × {qty}" for m, qty in haves),
                "color": DISCORD_COLORS["have"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "footer": {"text": "Arc Raider Material Tracker"},
            })

        payload = {"username": "Arc Raider Tracker", "embeds": embeds}
        self._set_status("Posting to Discord…")
        self._send_webhook(webhook_url, payload, success_msg="✅ Posted to Discord!")

    def _send_webhook(self, url: str, payload: dict, success_msg: str = "✅ Sent!"):
        """POST payload to a Discord webhook URL on a background thread."""
        def _do():
            try:
                r = requests.post(url, json=payload, timeout=10)
                if r.ok:
                    self.after(0, lambda: self._set_status(success_msg))
                else:
                    msg = f"Discord returned HTTP {r.status_code}: {r.reason}"
                    body = r.text.strip()
                    if body:
                        msg += f"\n\n{body}"
                    self.after(0, lambda: self._set_status(f"Discord error {r.status_code}"))
                    self.after(0, lambda: messagebox.showerror("Discord Error", msg))
            except Exception as exc:
                err = str(exc)
                self.after(0, lambda: self._set_status("Failed to post."))
                self.after(0, lambda: messagebox.showerror("Connection Error", err))

        threading.Thread(target=_do, daemon=True).start()

    # ── Dialogs ────────────────────────────────────────────────────────────────

    def _open_settings(self):
        def save(url):
            self._config["webhook_url"] = url
            self._config["player_name"] = self.player_name_var.get().strip()
            self._save_json(CONFIG_FILE, self._config)
            self._set_status("Settings saved.")

        def test(url, callback):
            payload = {
                "username": "Arc Raider Tracker",
                "content": "✅ Webhook test — connection is working!",
            }
            def _do():
                try:
                    r = requests.post(url, json=payload, timeout=10)
                    if r.ok:
                        self.after(0, lambda: callback(True, ""))
                    else:
                        detail = f"HTTP {r.status_code}: {r.reason}"
                        body = r.text.strip()
                        if body:
                            detail += f" — {body}"
                        self.after(0, lambda: callback(False, detail))
                except Exception as exc:
                    self.after(0, lambda: callback(False, str(exc)))
            threading.Thread(target=_do, daemon=True).start()

        SettingsDialog(self, self._config, save, test)

    def _open_materials_manager(self):
        def save(new_list):
            self.materials = new_list
            self._save_json(MATERIALS_FILE, new_list)
            # Purge saved data for removed materials
            self._player_data = {m: v for m, v in self._player_data.items() if m in new_list}
            self._build_material_rows()
            self._set_status("Material list updated.")

        MaterialsManagerDialog(self, self.materials, save)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _set_status(self, msg: str):
        self.status_var.set(msg)


if __name__ == "__main__":
    app = App()
    app.mainloop()
