#!/usr/bin/env python3
print("STARTING deleteMe")
print("1. Before animation")
show_fake_hack_animation()
print("2. After animation")
welcome()
print("3. After welcome")
first_time_setup()
print("4. After setup")

"""
deleteMe v4 — Digital-footprint scrubbing assistant
with debugging & logging.

Author: William “TwoWheelJunky” Peterson
"""

import csv
import random
import webbrowser
import logging
import time, os, socket, requests
from pathlib import Path

# ----------------------------- CONFIG ----------------------------- #
BROKER_CSV       = Path(__file__).with_name("brokers.csv")
OFFLINE_QUOTES   = Path(__file__).with_name("motivational_quotes.txt")
CUSTOM_QUOTES    = Path(__file__).with_name("custom_quotes.txt")
ONLINE_URL       = ("https://raw.githubusercontent.com/logicalrock/"
                    "deleteMe/main/quotes/official_quotes.txt")
MAX_LOCAL_QUOTES = 100

PAID_SERVICES  = ["Incogni", "DeleteMe", "Kanary", "Optery", "OneRep"]
FREE_SERVICES  = ["SimpleOptOut", "JustDeleteMe", "StopDataBrokers"]

DEBUG = True  # Toggle for console debug output

# --------------------------- LOGGER ------------------------------- #
logging.basicConfig(
    filename='deleteMe.log',
    filemode='a',
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.DEBUG
)

def debug(msg):
    logging.debug(msg)
    if DEBUG:
        print(f"[DEBUG] {msg}")

# --------------------------- GLOBALS ------------------------------ #
user_name     = "Friend"
user_services = []
quotes_cache  = []

# ------------------------- FAKE HACK FX --------------------------- #
def show_fake_hack_animation():
    frames = [
        "💀💀💀  YOUR DATA IS MINE!!  💀💀💀",
        "💀💀💀  JUST KIDDING 😄      💀💀💀",
        "💀💀💀  Launching deleteMe  💀💀💀"
    ]
    for i in range(6):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n" * 5)
        print("".center(80, "="))
        print(frames[i % len(frames)].center(80))
        print("".center(80, "="))
        time.sleep(1)

# --------------------------- QUOTES ------------------------------ #
def load_quotes():
    debug("Loading quotes...")
    quotes = []

    def add_from_file(path):
        if path.exists():
            raw = path.read_text(encoding="utf-8")
            quotes.extend([q.strip() for q in raw.split('%') if q.strip()])

    add_from_file(OFFLINE_QUOTES)
    add_from_file(CUSTOM_QUOTES)
    del quotes[MAX_LOCAL_QUOTES:]

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        resp = requests.get(ONLINE_URL, timeout=3)
        if resp.ok:
            online_quotes = [q.strip() for q in resp.text.split('%') if q.strip()]
            quotes.extend(online_quotes)
            debug(f"Fetched {len(online_quotes)} online quotes")
    except Exception as e:
        debug(f"Online quote fetch failed: {e}")

    debug(f"Total quotes loaded: {len(quotes)}")
    return quotes

def show_quote():
    if quotes_cache:
        quote = random.choice(quotes_cache)
        print("\n🗣️  Inspiration:")
        print(quote + "\n")
        debug(f"Displayed quote: {quote[:60]}...")

# -------------------------- BROKERS ------------------------------ #
def load_brokers():
    debug("Loading brokers.csv")
    if not BROKER_CSV.exists():
        debug("brokers.csv missing!")
        return []
    with BROKER_CSV.open(newline='', encoding='utf-8') as fh:
        brokers = list(csv.DictReader(fh))
    debug(f"Loaded {len(brokers)} brokers")
    return brokers

def save_brokers(brokers):
    if not brokers:
        return
    fieldnames = brokers[0].keys()
    with BROKER_CSV.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(brokers)
    debug("Saved brokers.csv")

def sort_and_label_brokers(brokers):
    uncovered, covered = [], []
    for b in brokers:
        service_done = bool(b.get("covered_by"))
        manual_done  = b.get("status", "").lower() == "completed"
        if service_done:
            b["label"] = f"✅ {b['name']}"
            covered.append(b)
        elif manual_done:
            b["label"] = f"🟡 {b['name']}"
            covered.append(b)
        else:
            b["label"] = b["name"]
            uncovered.append(b)
    uncovered.sort(key=lambda x: x["name"].lower())
    covered.sort(key=lambda x: x["name"].lower())
    return uncovered, covered

def auto_mark_covered(brokers):
    debug("Auto-marking covered brokers")
    for b in brokers:
        if any(svc.lower() in (b.get("covered_by") or "").lower()
               for svc in user_services):
            b["covered_by"] = b.get("covered_by") or ",".join(user_services)
    return brokers

# ------------------------- UI FUNCTIONS -------------------------- #
def welcome():
    global user_name
    print("\n🧹  Welcome to deleteMe!\n")
    print("This tool will guide you—step by step—through removing your personal")
    print("information from dozens of data-broker websites.\n")
    user_name = input("Before we begin, what’s your name? ").strip() or "Friend"
    print(f"\nGreat to meet you, {user_name}! Let’s get started.\n")
    debug(f"user_name set to {user_name}")

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
    debug(f"user_services = {user_services}")
    show_quote()

def view_brokers(brokers):
    uncovered, covered = sort_and_label_brokers(brokers)
    debug(f"view_brokers(): {len(uncovered)} uncovered, {len(covered)} covered")

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

def add_broker(brokers):
    try:
        name = input("Broker name (e.g., DataScrub Corp): ").strip()
        if not name:
            print("⚠️  Name cannot be empty.")
            return
        debug(f"User entered broker name: {name}")

        link = input("Opt-out link (e.g., https://example.com/opt-out): ").strip()
        if not link.startswith("http"):
            print("⚠️  Invalid link. Must start with http or https.")
            return
        debug(f"User entered link: {link}")

        brokers.append({
            "name": name,
            "opt_out_link": link,
            "covered_by": "",
            "status": "Pending"
        })
        save_brokers(brokers)
        print(f"🟡 {name} added and marked as Pending.")
        show_quote()
    except Exception as e:
        logging.exception("Failed to add broker")
        print("❌ Something went wrong while adding the broker. See deleteMe.log.")

def open_opt_out(brokers):
    uncovered, _ = sort_and_label_brokers(brokers)
    if not uncovered:
        print(f"Nice work, {user_name}! There are no remaining brokers.")
        return

    view_brokers(brokers)
    try:
        choice = int(input("Enter broker number to open its opt-out link: "))
        target = uncovered[choice]
        debug(f"User selected broker index {choice}: {target['name']}")
        webbrowser.open(target['opt_out_link'])
        target["status"] = "Completed"
        save_brokers(brokers)
        print("Marked as Completed 🟡")
        show_quote()
    except (IndexError, ValueError):
        print("Invalid selection.")

# ----------------------------- MAIN ------------------------------- #
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
