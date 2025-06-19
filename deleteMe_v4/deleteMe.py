import csv
import os
import webbrowser

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
    print("Let's set up your removal support options:")
    for s in PAID_SERVICES:
        response = input(f"Do you use {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    for s in FREE_SERVICES:
        response = input(f"Would you like to include free service {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    print(f"Thanks! We'll account for these services: {user_services}")

def auto_mark_covered(brokers):
    for b in brokers:
        for svc in user_services:
            if svc.lower() in b['opt_out_link'].lower():
                b['covered_by'] = svc
    return brokers

def view_brokers(brokers):
    print("\nFiltered broker list (skipping covered ones):")
    for idx, b in enumerate(brokers):
        if b.get('covered_by'):
            continue
        print(f"[{idx}] {b['name']} – {b['opt_out_link']}")
    print()

def open_opt_out(brokers):
    view_brokers(brokers)
    try:
        choice = int(input("Enter broker number to open opt-out link: "))
        url = brokers[choice]['opt_out_link']
        print(f"Opening: {url}")
        webbrowser.open(url)
    except (IndexError, ValueError):
        print("Invalid selection.")

def add_broker(brokers):
    name = input("Broker name: ")
    link = input("Opt-out link: ")
    new_entry = {"name": name, "opt_out_link": link, "covered_by": ""}
    brokers.append(new_entry)
    save_brokers(brokers)
    print(f"{name} added.")

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
