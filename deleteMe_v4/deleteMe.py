
#!/usr/bin/env python3

import os
import csv
import time
import logging
import random
import webbrowser
import signal
from platformdirs import user_data_dir

# Logging config
logging.basicConfig(
    filename='./deleteMe.log',
    filemode='a',
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.DEBUG
)

def debug(msg):
    logging.debug(msg)
    print(f"[DEBUG] {msg}")

# Set up app-specific directories
APP_NAME = "deleteMe"
APP_AUTHOR = "logicalrock"
data_dir = user_data_dir(APP_NAME, APP_AUTHOR)
os.makedirs(data_dir, exist_ok=True)

# Globals
user_name = ""
user_services = []
BROKERS_FILE = ""
PAID_SERVICES = ["Incogni", "DeleteMe", "Kanary", "Optery", "OneRep"]
FREE_SERVICES = ["SimpleOptOut", "JustDeleteMe", "StopDataBrokers"]
QUOTES_FILE = "motivational_quotes.txt"

def signal_handler(sig, frame):
    print("\n❌ Program interrupted. Exiting gracefully.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def show_fake_hack_animation():
    frames = [
        "💀💀💀  YOUR DATA IS MINE!!  💀💀💀",
        "💀💀💀  JUST KIDDING 😄      💀💀💀",
        "💀💀💀  Launching deleteMe  💀💀💀"
    ]
    for _ in range(2):
        for frame in frames:
            os.system("cls" if os.name == "nt" else "clear")
            print("\n" * 3)
            print("=" * 80)
            print(frame.center(80))
            print("=" * 80)
            print("\n" * 3)
            time.sleep(1.5)

def setup_user_file():
    global BROKERS_FILE
    safe_name = ''.join(c for c in user_name if c.isalnum())
    BROKERS_FILE = os.path.join(data_dir, f"deleteMe_brokers_{safe_name}.csv")
    debug(f"Using broker file for user {user_name} at: {BROKERS_FILE}")

def load_brokers():
    brokers = []
    if not os.path.exists(BROKERS_FILE):
        debug(f"{BROKERS_FILE} not found; creating new one.")
        with open(BROKERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'opt_out_link', 'covered_by', 'completed'])
            writer.writeheader()
        return brokers

    with open(BROKERS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            broker = {
                'name': row.get('name', '').strip(),
                'opt_out_link': row.get('opt_out_link', '').strip(),
                'covered_by': row.get('covered_by', '').strip(),
                'completed': row.get('completed', 'False').strip().lower() == 'true'
            }
            brokers.append(broker)

    debug(f"Loaded {len(brokers)} brokers")
    return brokers

def save_brokers(brokers):
    with open(BROKERS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'opt_out_link', 'covered_by', 'completed'])
        writer.writeheader()
        for b in brokers:
            writer.writerow({
                'name': b['name'],
                'opt_out_link': b['opt_out_link'],
                'covered_by': b.get('covered_by', ''),
                'completed': b.get('completed', False)
            })

def show_quote():
    try:
        with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
            quotes = [line.strip() for line in f if line.strip()]
        if quotes:
            print("\n🧠 ", random.choice(quotes))
    except Exception as e:
        logging.warning(f"Failed to load quote: {e}")

def welcome():
    global user_name
    print("STARTING deleteMe")
    debug("1. Before animation")
    show_fake_hack_animation()
    debug("2. After animation")

    print("🧹  Welcome to deleteMe!")
    print("""
This tool will guide you—step by step—through removing your personal
information from dozens of data-broker websites.
""")
    debug("Waiting for input: Before we begin, what’s your name?")
    user_name = input("Before we begin, what’s your name? ").strip()
    print(f"\nGreat to meet you, {user_name}! Let’s get started.\n")

def first_time_setup():
    global user_services
    print(f"\n{user_name}, let's set up your removal support options:\n")
    for s in PAID_SERVICES:
        response = input(f"Do you use {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    for s in FREE_SERVICES:
        response = input(f"Include free helper {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    print(f"\nThank you, {user_name}! We’ll use these services to guide your opt-outs:")
    print(f"🛡️  Services selected: {user_services}\n")
    debug(f"Services selected: {user_services}")

def view_brokers(brokers):
    print(f"\n{user_name}, here’s an overview of data-broker sites:")
    uncovered = [b for b in brokers if not b.get('covered_by')]
    covered = [b for b in brokers if b.get('covered_by')]

    print(f"• Brokers still needing manual opt-out: {len(uncovered)}")
    print(f"• Already completed / covered: {len(covered)}\n")

    if uncovered:
        print("👉 Brokers you may want to tackle next:")
        for idx, b in enumerate(uncovered):
            print(f"[{idx}] {b['name']} – {b['opt_out_link']}")
    else:
        print("🎉 No uncovered brokers left!")

    if covered:
        print("\n✓ Brokers already handled:")
        for b in covered:
            color = "✅" if b['covered_by'] in PAID_SERVICES + FREE_SERVICES else "🟡"
            print(f"   {color} {b['name']}")
    print()
    show_quote()

def open_opt_out(brokers):
    pending = [b for b in brokers if not b.get('covered_by')]
    if not pending:
        print(f"Nice work, {user_name}! There are no remaining brokers.\n")
        return

    for idx, b in enumerate(pending):
        print(f"[{idx}] {b['name']} – {b['opt_out_link']}")
    print()

    choice_str = input("Which broker would you like to open? (#): ").strip()
    if not choice_str.isdigit():
        print("❌ Please enter a valid number shown in the list.")
        return

    choice = int(choice_str)
    if not 0 <= choice < len(pending):
        print("❌ Invalid choice. Pick a number from the list.")
        return

    broker = pending[choice]
    print(f"🌐 Opening: {broker['name']} – {broker['opt_out_link']}")
    webbrowser.open(broker['opt_out_link'])

    response = input(f"Did you complete the opt-out for {broker['name']}? (y/n): ").lower()
    if response == 'y':
        broker['covered_by'] = "manual"
        debug(f"Marked {broker['name']} as manually completed.")
        save_brokers(brokers)
        print("✅ Marked as complete!")
        show_quote()

def add_broker(brokers):
    name = input("Broker name: ").strip()
    link = input("Opt-out link: ").strip()
    brokers.append({"name": name, "opt_out_link": link, "covered_by": ""})
    save_brokers(brokers)
    print(f"✅ Added broker: {name}")
    show_quote()

def main_menu():
    brokers = load_brokers()
    while True:
        print("Options:")
        print("1. View brokers")
        print("2. Launch opt-out")
        print("3. Add broker")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            view_brokers(brokers)
        elif choice == '2':
            open_opt_out(brokers)
        elif choice == '3':
            add_broker(brokers)
        elif choice == '4':
            print(f"Goodbye, {user_name} 👋")
            break
        else:
            print("❌ Invalid option. Try again.")
        print()

if __name__ == "__main__":
    welcome()
    setup_user_file()
    first_time_setup()
    main_menu()
