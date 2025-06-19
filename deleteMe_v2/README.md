# 🧹 Footprint Scrubber

Footprint Scrubber helps you erase your digital footprint **with or without paid data‑removal services**.

## 🚀 Key Features

- **Paid‑Service Awareness** – Detects your subscriptions (Incogni, DeleteMe, Kanary, Optery, OneRep) and skips brokers they already cover.
- **Free Resource Launcher** – Opens popular free opt‑out aggregators (SimpleOptOut, JustDelete.me, StopDataBrokers).
- **Encrypted Personal Data** – Uses `cryptography` (optional) to store your identifiers locally.
- **CSV‑Driven Broker List** – Manage hundreds of brokers in `brokers.csv` with `covered_by` + `status` columns.
- **Email & URL Automation** – One‑click opt‑out links and pre‑drafted email templates for brokers needing email requests.

## 🛠 Setup

```bash
pip install cryptography   # optional but recommended
python3 footprint_scrubber.py
```

### First‑Run Wizard
1. Choose your **paid services** (Incogni, DeleteMe, Kanary, Optery, OneRep).  
2. Decide whether to integrate **free / open‑source** resources.  
3. Preferences save to `scrubber_config.json`.

## 📋 brokers.csv Columns

| Column      | Purpose                                                      |
|-------------|--------------------------------------------------------------|
| `name`      | Broker / data‑broker name                                    |
| `url`       | Direct opt‑out or privacy request form                       |
| `email`     | Privacy email address (if form absent)                       |
| `notes`     | Requirements (CAPTCHA, ID needed, etc.)                      |
| `covered_by`| Semicolon‑separated list of paid services covering this broker (`incogni;deleteme`) |
| `status`    | Your progress (`Pending`, `Submitted`, `Completed`)          |

## 💡 Tips

- Expand `brokers.csv` with lists from SimpleOptOut or Yael Writes’ “Big‑Ass Data Broker” spreadsheet.
- Re‑run the setup wizard anytime to update your service subscriptions.

## ⚠️ Disclaimer
This tool assists your privacy journey but cannot guarantee compliance across all brokers. Always verify each removal manually.

© 2025 William “TwoWheelJunky” Peterson
