import csv
import os
import webbrowser
import random
from pathlib import Path

# Adding user interaction and context for deleteMe

user_name = "Friend"   # fallback

def welcome():
    global user_name
    print("\n🧹  Welcome to deleteMe!\n")
    print("This tool will guide you step-by-step through removing your personal")
    print("information from dozens of data-broker websites. You’ll answer a few")
    print("simple questions first; then we’ll show you clear options and links.\n")
    user_name = input("Before we begin, what’s your name? ").strip() or "Friend"
    print(f"\nGreat to meet you, {user_name}! Let’s get started.\n")

def sort_and_label_brokers(brokers):
    """
    Returns two lists:
    1. uncovered – still needing action
    2. covered   – already handled
    Adds a 'label' to each broker:
      - ✅ if covered_by is set
      - 🟡 if status is 'completed' (manual)
    """
    uncovered, covered = [], []

    for b in brokers:
        is_covered = bool(b.get("covered_by"))
        is_manual_done = b.get("status", "").lower() == "completed"

        if is_covered:
            b["label"] = f"✅ {b['name']}"
            covered.append(b)
        elif is_manual_done:
            b["label"] = f"🟡 {b['name']}"
            covered.append(b)
        else:
            b["label"] = b["name"]
            uncovered.append(b)

    uncovered.sort(key=lambda x: x["name"].lower())
    covered.sort(key=lambda x: x["name"].lower())
    return uncovered, covered

# Motivatonal quotes for the user

QUOTES_FILE = Path(__file__).with_name("motivational_quotes.txt")

def load_quotes():
    if QUOTES_FILE.exists():
        # quotes separated by a line containing just %
        with open(QUOTES_FILE, encoding="utf-8") as f:
            return [q.strip() for q in f.read().split('%') if q.strip()]
    return []

QUOTES = load_quotes()

def show_quote():
    """Print a random motivational quote, if list is available."""
    if QUOTES:
        print("\n🗣️  Inspiration:")
        print(random.choice(QUOTES))
        print()

# ── Call the new function at the start of main() ──
def main():
    welcome()                     # ← NEW
    first_time_setup()
    brokers = load_brokers()
    brokers = auto_mark_covered(brokers)
    ...


BROKER_CSV = "brokers.csv"
PAID_SERVICES = ["Incogni", "DeleteMe", "Privacy Bee"]
FREE_SERVICES = ["SimpleOptOut", "JustDeleteMe"]

user_services = []

def load_brokers():
    brokers = []
    if not os.path.exists(BROKER_CSV):
        return brokers
    with open(BROKER_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            brokers.append(row)
    return brokers

def save_brokers(brokers):
    if not brokers:
        return
    fieldnames = brokers[0].keys()
    with open(BROKER_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(brokers)

def first_time_setup():
    print(f"\n{user_name}, let's set up your removal support options:")
    for s in PAID_SERVICES:
        response = input(f"Do you use {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    for s in FREE_SERVICES:
        response = input(f"Would you like to include free service {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    
    # 👇 Personalized message here
    print(f"\nThank you, {user_name}! We'll use these services to help guide your opt-outs:")
    print(f"🛡️  Services selected: {user_services}")


def auto_mark_covered(brokers):
    for b in brokers:
        for svc in user_services:
            if svc.lower() in b['opt_out_link'].lower():
                b['covered_by'] = svc
    return brokers

def view_brokers(brokers):
    uncovered, covered = sort_and_label_brokers(brokers)
    total_uncovered = len(uncovered)

    print(f"\n{user_name}, here’s an overview of data-broker sites:")
    print(f"• Brokers still needing manual opt-out: {total_uncovered}")
    print(f"• Already completed / covered: {len(covered)}\n")

# Show uncovered first
    if uncovered:
        print("👉 Brokers you may want to tackle next:")
        for idx, b in enumerate(uncovered):
            print(f"[{idx}] {b['label']} – {b['opt_out_link']}")
    else:
        print("🎉 No uncovered brokers left!")

    # Optionally list covered/completed ones too
    if covered:
        print("\n✓ Brokers already handled:")
        for b in covered:
            print(f"   {b['label']}")

    print()

def open_opt_out(brokers):
    uncovered, _ = sort_and_label_brokers(brokers)
    view_brokers(brokers)  # optional: remind user of list

    if not uncovered:
        print(f"Nice work, {user_name}! There are no remaining brokers.")
        return

    try:
        choice = int(input("Enter broker number to open its opt-out link: "))
        url = uncovered[choice]['opt_out_link']
        print(f"Opening: {url}")
        webbrowser.open(url)
    except (IndexError, ValueError):
        print("Invalid selection.")

def add_broker(brokers):
    name = input("Broker name: ").strip()
    link = input("Opt-out link: ").strip()
    new_entry = {
        "name": name,
        "opt_out_link": link,
        "covered_by": "",
        "status": "Pending"
    }
    brokers.append(new_entry)
    save_brokers(brokers)
    print(f"{name} added and marked as Pending.")


def main():
    print("Welcome to deleteMe – your digital footprint scrubber!\n")
    first_time_setup()
    brokers = load_brokers()
    brokers = auto_mark_covered(brokers)

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
