#!/usr/bin/env python3
"""footprint_scrubber.py

Digital‑footprint eraser helper with paid/free service integration.

Highlights
----------
* Detects your paid data‑removal subscriptions (Incogni, DeleteMe, Kanary, Optery, OneRep).
* Skips brokers already covered by those services (via `covered_by` column in `brokers.csv`).
* Recommends and optionally opens free/open‑source opt‑out aggregators.
* Interactive CLI, encrypted storage, progress tracking.

Author: William “TwoWheelJunky” Peterson, 2025‑06‑19
"""

import csv
import json
import webbrowser
from pathlib import Path

# Optional encryption
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

APP_DIR = Path(__file__).resolve().parent
BROKERS_FILE = APP_DIR / "brokers.csv"
USER_DATA_FILE = APP_DIR / "user_data.enc"
CONFIG_FILE = APP_DIR / "scrubber_config.json"

PAID_SERVICES = ["Incogni", "DeleteMe", "Kanary", "Optery", "OneRep"]
FREE_SERVICES = {
    "SimpleOptOut": "https://simpleoptout.com",
    "JustDelete.me": "https://justdelete.me",
    "StopDataBrokers": "https://stopdatabrokers.com",
}

# -----------------------------------------------------------------------------
# General helpers
# -----------------------------------------------------------------------------
def _print_banner():
    print("\n=== Footprint Scrubber ===\n")

def _pause():
    input("\nPress <Enter> to continue...")

def _yes_no(prompt: str) -> bool:
    return input(prompt + " (y/n): ").strip().lower().startswith('y')

# -----------------------------------------------------------------------------
# Configuration wizard
# -----------------------------------------------------------------------------
def _setup_wizard():
    print("Let's set up your services.\n")
    cfg = {"paid_services": [], "free_services": []}

    if _yes_no("Do you use any PAID data‑removal services (e.g., Incogni, DeleteMe)?"):
        print("Select from the list below. Enter numbers separated by commas (or press Enter to skip).\n")
        for idx, svc in enumerate(PAID_SERVICES, 1):
            print(f" {idx}. {svc}")
        choice = input("Selection: ").strip()
        if choice:
            for num in choice.split(','):
                try:
                    svc = PAID_SERVICES[int(num) - 1]
                    cfg["paid_services"].append(svc)
                except (ValueError, IndexError):
                    pass

    if _yes_no("Would you like to integrate RECOMMENDED FREE / open‑source helper sites?"):
        print("Great! We'll include the following:")
        for name in FREE_SERVICES:
            print(" -", name)
        cfg["free_services"] = list(FREE_SERVICES.keys())

    with CONFIG_FILE.open('w', encoding='utf-8') as fh:
        json.dump(cfg, fh, indent=2)
    print(f"Configuration saved ➜ {CONFIG_FILE}\n")
    return cfg

def load_config():
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open(encoding='utf-8') as fh:
            return json.load(fh)
    else:
        return _setup_wizard()

# -----------------------------------------------------------------------------
# Personal‑data functions
# -----------------------------------------------------------------------------
def collect_user_data():
    print("\nEnter the details you want the script to reference when filling requests.")
    user_data = {
        "full_name": input("Full legal name: ").strip(),
        "emails": [e.strip() for e in input("Email address(es) (comma‑sep): ").split(',') if e.strip()],
        "usernames": [u.strip() for u in input("Username(s)/alias(es) (comma‑sep): ").split(',') if u.strip()],
        "phone_numbers": [p.strip() for p in input("Phone number(s) (comma‑sep): ").split(',') if p.strip()],
        "addresses": [a.strip() for a in input("Current + past address(es) (comma‑sep): ").split(',') if a.strip()],
    }
    return user_data

def _encrypt_and_save(data: dict, path: Path):
    from cryptography.fernet import Fernet
    key_path = path.with_suffix('.key')
    if not key_path.exists():
        key = Fernet.generate_key()
        key_path.write_bytes(key)
    else:
        key = key_path.read_bytes()
    cipher = Fernet(key)
    token = cipher.encrypt(json.dumps(data).encode())
    path.write_bytes(token)

def _save_plain(data: dict, path: Path):
    path.write_text(json.dumps(data, indent=2))

def save_user_data(data: dict):
    if CRYPTO_AVAILABLE:
        _encrypt_and_save(data, USER_DATA_FILE)
        print(f"Encrypted user data saved ➜ {USER_DATA_FILE}")
    else:
        _save_plain(data, USER_DATA_FILE.with_suffix('.json'))
        print("cryptography not installed; saved unencrypted JSON. Install with 'pip install cryptography' for encryption.")

# -----------------------------------------------------------------------------
# Broker helpers
# -----------------------------------------------------------------------------
def load_brokers():
    # CSV columns: name,url,email,notes,covered_by,status
    if not BROKERS_FILE.exists():
        print(f"Broker list not found: {BROKERS_FILE}")
        return []
    with BROKERS_FILE.open(newline='', encoding='utf‑8') as fh:
        reader = csv.DictReader(fh)
        return list(reader)

def _filter_brokers(brokers, paid_services):
    if not paid_services:
        return brokers
    ps = {s.lower() for s in paid_services}
    filtered = []
    for b in brokers:
        covered = {svc.strip().lower() for svc in b.get('covered_by', '').split(';') if svc.strip()}
        if not covered.intersection(ps):
            filtered.append(b)
    return filtered

def open_opt_out_pages(brokers, paid_services):
    targets = _filter_brokers(brokers, paid_services)
    for b in targets:
        if b.get('url'):
            print(f"Opening {b['name']} : {b['url']}")
            webbrowser.open(b['url'])

def export_email_templates(brokers, user_data, paid_services):
    targets = _filter_brokers(brokers, paid_services)
    out_dir = APP_DIR / "emails"
    out_dir.mkdir(exist_ok=True)
    for b in targets:
        if b.get('email'):
            tpl = f"""Subject: Data Privacy Request – {user_data['full_name']}

Dear {b['name']} Privacy Team,

I am exercising my privacy rights and request the removal of my personal data from your systems.

Identifiers:
- Full name: {user_data['full_name']}
- Email(s): {', '.join(user_data['emails'])}
- Phone(s): {', '.join(user_data['phone_numbers'])}
- Address(es): {', '.join(user_data['addresses'])}

Please confirm once completed.

Sincerely,
{user_data['full_name']}
"""
            (out_dir / f"{b['name'].lower().replace(' ', '_')}.txt").write_text(tpl)
    print(f"Email drafts saved to ➜ {out_dir}")

def open_free_resources(free_services):
    for name in free_services:
        url = FREE_SERVICES.get(name)
        if url:
            print(f"Opening {name}: {url}")
            webbrowser.open(url)

# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def manage_services(cfg):
    while True:
        print("\n=== Manage Services ===")
        print("1. View current services")
        print("2. Add a paid service")
        print("3. Remove a paid service")
        print("4. Add a free/open-source resource")
        print("5. Remove a free resource")
        print("6. Back to main menu")
        choice = input("Select> ").strip()

        if choice == '1':
            print("\nCurrent paid services:", cfg.get("paid_services", []))
            print("Current free resources:", cfg.get("free_services", []))
        elif choice == '2':
            name = input("Enter name of the paid service to add: ").strip()
            if name and name not in cfg["paid_services"]:
                cfg["paid_services"].append(name)
        elif choice == '3':
            name = input("Enter name of the paid service to remove: ").strip()
            if name in cfg["paid_services"]:
                cfg["paid_services"].remove(name)
        elif choice == '4':
            name = input("Enter name of the free service to add: ").strip()
            url = input("Enter URL for the free service: ").strip()
            if name and url:
                if name not in cfg["free_services"]:
                    cfg["free_services"].append(name)
                if name not in FREE_SERVICES:
                    FREE_SERVICES[name] = url
        elif choice == '5':
            name = input("Enter name of the free service to remove: ").strip()
            if name in cfg["free_services"]:
                cfg["free_services"].remove(name)
                FREE_SERVICES.pop(name, None)
        elif choice == '6':
            with CONFIG_FILE.open('w', encoding='utf-8') as fh:
                json.dump(cfg, fh, indent=2)
            break
        else:
            print("Invalid selection.")

def main_menu():
    cfg = load_config()
        elif choice == '6':
            manage_services(cfg)
    paid = cfg.get('paid_services', [])
    free = cfg.get('free_services', [])

    while True:
        _print_banner()
        print("Paid services detected:", paid if paid else "None")
        print("Free services selected:", free if free else "None")
        print("\n1. Collect & save personal data")
        print("2. Launch opt‑out URLs (excluding paid‑service coverage)")
        print("3. Generate email templates (excluding paid‑service coverage)")
        print("4. Open recommended free resources")
        print("5. Re‑run setup wizard")
        print("6. Manage services")
        print("7. Quit")

        if choice == '1':
            data = collect_user_data()
            save_user_data(data)
            _pause()
        elif choice == '2':
            brokers = load_brokers()
            open_opt_out_pages(brokers, [s.lower() for s in paid])
            _pause()
        elif choice == '3':
            if not USER_DATA_FILE.exists():
                print("No stored user data found; run option 1 first.")
            else:
                if CRYPTO_AVAILABLE:
                    from cryptography.fernet import Fernet
                    key_path = USER_DATA_FILE.with_suffix('.key')
                    key = key_path.read_bytes()
                    cipher = Fernet(key)
                    data = json.loads(cipher.decrypt(USER_DATA_FILE.read_bytes()).decode())
                else:
                    data = json.loads(USER_DATA_FILE.with_suffix('.json').read_text())
                brokers = load_brokers()
                export_email_templates(brokers, data, [s.lower() for s in paid])
            _pause()
        elif choice == '4':
            open_free_resources(free)
            _pause()
        elif choice == '5':
            cfg = _setup_wizard()
            paid = cfg.get('paid_services', [])
        elif choice == '6':
            manage_services(cfg)
            free = cfg.get('free_services', [])
        elif choice == '7':
            break
        else:
            print("Invalid selection.")
            _pause()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nBye.")