#!/usr/bin/env python3
print("STARTING deleteMe")

import os
import csv
import time
import random
import requests
import logging

DEBUG = True
user_name = ""
user_services = []
quotes_cache = []

PAID_SERVICES = ["Incogni", "DeleteMe", "Kanary", "Optery", "OneRep"]
FREE_SERVICES = ["SimpleOptOut", "JustDeleteMe", "StopDataBrokers"]

# Logging config
logging.basicConfig(
    filename='deleteMe.log',
    filemode='a',
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.DEBUG
)

def debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")
    logging.debug(msg)

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

def welcome():
    global user_name
    print("\n🧹  Welcome to deleteMe!\n")
    print("This tool will guide you—step by step—through removing your personal")
    print("information from dozens of data-broker websites.\n")
    user_name = input("Before we begin, what’s your name? ").strip()
    print(f"\nGreat to meet you, {user_name}! Let’s get started.\n")
    debug(f"User name set to: {user_name}")

def first_time_setup():
    print(f"\n{user_name}, let's set up your removal support options:")
    for s in PAID_SERVICES:
        response = input(f"Do you use {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    for s in FREE_SERVICES:
        response = input(f"Include free helper {s}? (y/n): ").lower()
        if response == 'y':
            user_services.append(s)
    print(f"\nThank you, {user_name}! We’ll use these services to guide your opt-outs:")
    print(f"🛡️  Services selected: {user_services}")
    debug(f"Services selected: {user_services}")

def load_brokers():
    brokers = []
    try:
        with open("brokers.csv", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                brokers.append(row)
        debug(f"Loaded {len(brokers)} brokers from CSV.")
    except Exception as e:
        logging.exception("Failed to load brokers.")
    return brokers

def save_brokers(brokers):
    try:
        with open("brokers.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "opt_out_link", "covered_by", "status"])
            writer.writeheader()
            writer.writerows(brokers)
        debug("Saved brokers to CSV.")
    except Exception as e:
        logging.exception("Failed to save brokers.")

def auto_mark_covered(brokers):
    for broker in brokers:
        if broker["covered_by"] in user_services:
            broker["status"] = "Complete"
    return brokers

def view_brokers(brokers):
    print(f"\n{user_name}, here’s an overview of data-broker sites:")
    uncovered = [b for b in brokers if b.get("status") != "Complete"]
    covered = [b for b in brokers if b.get("status") == "Complete"]
    print(f"• Brokers still needing manual opt-out: {len(uncovered)}")
    print(f"• Already completed / covered: {len(covered)}\n")
    if uncovered:
        print("👉 Brokers you may want to tackle next:")
        for idx, b in enumerate(sorted(uncovered, key=lambda x: x['name'])):
            print(f"[{idx}] {b['name']} – {b['opt_out_link']}")
    else:
        print("🎉 No uncovered brokers left!")
    if covered:
        print("\n✓ Brokers already handled:")
        for b in sorted(covered, key=lambda x: x['name']):
            print(f"   ✅ {b['name']}")
    print()

def open_opt_out(brokers):
    pending = [b for b in brokers if b.get("status") != "Complete"]
    if not pending:
        print(f"Nice work, {user_name}! There are no remaining brokers.")
        return
    for idx, b in enumerate(pending):
        print(f"[{idx}] {b['name']} – {b['opt_out_link']}")
    try:
        choice = int(input("Choose a broker to open (or -1 to cancel): "))
        if choice == -1:
            return
        broker = pending[choice]
        os.system(f"open '{broker['opt_out_link']}'" if os.name == "posix" else f"start {broker['opt_out_link']}")
        confirm = input(f"Did you complete the opt-out for {broker['name']}? (y/n): ").lower()
        if confirm == 'y':
            broker['status'] = "Complete"
            save_brokers(brokers)
            print(f"🟡 Marked {broker['name']} as Complete.")
            show_quote()
    except Exception as e:
        logging.exception("Failed during opt-out step.")

def add_broker(brokers):
    try:
        name = input("Broker name (e.g., DataScrub Corp): ").strip()
        link = input("Opt-out link (e.g., https://example.com/opt-out): ").strip()
        if not name or not link:
            print("⚠️  Name and link must not be empty.")
            return
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
        logging.exception("Failed to add broker.")

def load_quotes():
    try:
        with open("motivational_quotes.txt") as f:
            return [q.strip() for q in f.readlines() if q.strip()]
    except:
        return []

def fetch_online_quote():
    try:
        res = requests.get("https://raw.githubusercontent.com/logicalrock/deleteMe/main/deleteMe_v4/motivational_quotes.txt", timeout=3)
        quotes = res.text.strip().split("\n")
        return random.choice(quotes)
    except:
        return random.choice(quotes_cache) if quotes_cache else "Keep going, you're doing great!"

def show_quote():
    print()
    print("📜", fetch_online_quote())
    print()

def main():
    global quotes_cache
    print("1. Before animation")
    show_fake_hack_animation()
    print("2. After animation")
    welcome()
    print("3. After welcome")
    first_time_setup()
    print("4. After setup")
    brokers = auto_mark_covered(load_brokers())
    quotes_cache = load_quotes()
    while True:
        print("\nOptions:")
        print("1. View brokers")
        print("2. Launch opt-out")
        print("3. Add broker")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            view_brokers(brokers)
        elif choice == "2":
            open_opt_out(brokers)
        elif choice == "3":
            add_broker(brokers)
        elif choice == "4":
            print("👋 Exiting. Your progress has been saved.")
            break

if __name__ == "__main__":
    main()