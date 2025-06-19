#!/usr/bin/env python3
"""
deleteMe v4 – Digital-footprint scrubbing assistant.

Features
--------
• Personalized welcome (asks for user’s name)
• Service-aware setup (Incogni, DeleteMe, etc.)
• Broker list sorted alphabetically
• ✅ = covered by service   🟡 = manually completed
• Offline + online motivational quotes (IC authors only)

Author: William “TwoWheelJunky” Peterson
"""

import csv
import os
import time
import webbrowser
import random
from pathlib import Path

# -----------------------------  CONFIG  ----------------------------- #
BROKER_CSV      = Path(__file__).with_name("brokers.csv")
OFFLINE_QUOTES  = Path(__file__).with_name("motivational_quotes.txt")
CUSTOM_QUOTES   = Path(__file__).with_name("custom_quotes.txt")
ONLINE_URL      = ("https://raw.githubusercontent.com/logicalrock/"
                   "deleteMe/main/quotes/official_quotes.txt")
MAX_LOCAL_QUOTES = 100

PAID_SERVICES  = ["Incogni", "DeleteMe", "Kanary", "Optery", "OneRep"]
FREE_SERVICES  = ["SimpleOptOut", "JustDeleteMe", "StopDataBrokers"]

# ---------------------------  GLOBALS  ------------------------------ #
user_name       = "Friend"
user_services   = []
quotes_cache    = []

# ---------------------------  QUOTES  ------------------------------- #
def load_quotes():
    quotes = []

    def add_from_file(path):
        if path.exists():
            raw = path.read_text(encoding="utf-8")
            quotes.extend([q.strip() for q in raw.split('%') if q.strip()])

    # local fixed list
    add_from_file(OFFLINE_QUOTES)

    # optional user-provided list
    add_from_file(CUSTOM_QUOTES)

    # cap local list to MAX_LOCAL_QUOTES
    del quotes[MAX_LOCAL_QUOTES:]

    # try online list (silent fail)
    try:
        import requests, socket
        # covert connectivity test – ping Google DNS via socket (no HTTP)
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        resp = requests.get(ONLINE_URL, timeout=3)
        if resp.ok:
            online_quotes = [q.strip() for q in resp.text.split('%') if q.strip()]
            quotes.extend(online_quotes)
    except Exception:
        pass

    return quotes

def show_quote():
    if quotes_cache:
        print("\n🗣️  Inspiration:")
        print(random.choice(quotes_cache))
        print()

# ---------------------------  BROKERS  ------------------------------ #
def load_brokers():
    if not BROKER_CSV.exists():
        return []
    with BROKER_CSV.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))

def save_brokers(brokers):
    if not brokers:
        return
    fieldnames = brokers[0].keys()
    with BROKER_CSV.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(brokers)

def sort_and_label_brokers(brokers):
    uncovered, covered = [], []
    for b in brokers:
        is_service = bool(b.get("covered_by"))
        is_manual  = b.get("status", "").lower() == "completed"

        if is_service:
            b["label"] = f"✅ {b['name']}"
            covered.append(b)
        elif is_manual:
            b["label"] = f"🟡 {b['name']}"
            covered.append(b)
        else:
            b["label"] = b["name"]
            uncovered.append(b)

    uncovered.sort(key=lambda x: x["name"].lower())
    covered.sort(key=lambda x: x["name"].lower())
    return uncovered, covered

# ---------------------  You Have Been Hacked  ----------------------- #
def show_fake_hack_animation():
    frames = [
        r"💀💀💀   YOU HAVE BEEN HACKED   💀💀💀",
        r"💀💀💀   YOUR DATA IS MINE!!   💀💀💀",
        r"💀💀💀   JUST KIDDING 😄        💀💀💀",
        r"💀💀💀   Launching deleteMe... 💀💀💀"
    ]
    
    for i in range(10):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n" * 5)
        print("".center(80, "="))
        print(frames[i % len(frames)].center(80))
        print("".center(80, "="))
        time.sleep(1)

# -------------------------  UI FUNCTIONS  --------------------------- #
def welcome():
    global user_name
    print("\n🧹  Welcome to deleteMe!\n")
    print("This tool will guide you—step by step—through removing your personal")
    print("information from dozens of data-broker websites.\n")
    user_name = input("Before we begin, what’s your name? ").strip() or "Friend"
    print(f"\nGreat to meet you, {user_name}! Let’s get started.\n")

def first_time_setup():
    print(f"\n{user_name}, let's set up your removal support options:\n")
    for s in PAID_SERVICES:
        if input(f"Do you use {s}? (y/n): ").lower().startswith('y'):
            user_services.append(s)
    for s in FREE_SERVICES:
        if input(f"Include free helper {s}? (y/n): ").lower().startswith('y'):
            user_services.append(s)

    print(f"\nThank you, {user_name}! We’ll use these services to guide your opt-outs:")
    print(f"🛡️  Services selected: {user_services}")
    show_quote()

def auto_mark_covered(brokers):
    for b in brokers:
        if any(svc.lower() in (b.get("covered_by") or "").lower()
               for svc in user_services):
            b["covered_by"] = b.get("covered_by") or ",".join(user_services)
    return brokers

def view_brokers(brokers):
    uncovered, covered = sort_and_label_brokers(brokers)
    print(f"\n{user_name}, here’s an overview of data-broker sites:")
    print(f"• Brokers still needing manual opt-out: {len(uncovered)}")
    print(f"• Already completed / covered: {len(covered)}\n")

    if uncovered:
        print("👉 Brokers you may want to tackle next:")
        for idx, b in enumerate(uncovered):
            print(f"[{idx}] {b['label']} – {b['opt_out_link']}")
    else:
        print("🎉 No uncovered brokers left!")

    if covered:
        print("\n✓ Brokers already handled:")
        for b in covered:
            print(f"   {b['label']}")
    print()

def open_opt_out(brokers):
    uncovered, _ = sort_and_label_brokers(brokers)
    if not uncovered:
        print(f"Nice work, {user_name}! There are no remaining brokers.")
        return

    view_brokers(brokers)
    try:
        choice = int(input("Enter broker number to open its opt-out link: "))
        target = uncovered[choice]
        webbrowser.open(target['opt_out_link'])
        target["status"] = "Completed"
        save_brokers(brokers)
        print("Marked as Completed 🟡")
        show_quote()
    except (IndexError, ValueError):
        print("Invalid selection.")

def add_broker(brokers):
    name = input("Broker name: ").strip()
    link = input("Opt-out link: ").strip()
    brokers.append({
        "name": name, "opt_out_link": link,
        "covered_by": "", "status": "Pending"
    })
    save_brokers(brokers)
    print(f"{name} added and marked as Pending.")
    show_quote()

# -----------------------------  MAIN  ------------------------------- #
def main():
    global quotes_cache
    show_fake_hack_animation()
    welcome()
    first_time_setup()
    brokers = auto_mark_covered(load_brokers())
    quotes_cache = load_quotes()

    while True:
        print("\nOptions:")
        print("1. View brokers")
        print("2. Launch opt-out")
        print("3. Add broker")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            view_brokers(brokers)
        elif choice == '2':
            open_opt_out(brokers)
        elif choice == '3':
            add_broker(brokers)
        elif choice == '4':
            print(f"Goodbye, {user_name}! Stay safe online.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
