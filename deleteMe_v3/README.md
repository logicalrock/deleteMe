# 🧹 Footprint Scrubber (v3)

**Footprint Scrubber** is a fully interactive privacy automation tool that helps you reduce your digital footprint by working with or without paid data removal services.

---

## 🚀 New in Version 3

### ✅ Broker Editor (CLI-based)
- View all brokers in `brokers.csv`
- Add new brokers interactively (name, URL, email, notes, coverage, status)
- Update individual broker `status` (e.g., Pending → Completed)

### ✅ Auto-Marking Broker Coverage
- When you add a paid service via “Manage Services”, the tool will update all brokers to mark them as covered (updates the `covered_by` column)

---

## 🌐 Core Features

| Feature                    | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Paid-Service Awareness     | Detects and skips brokers already covered by Incogni, DeleteMe, etc.       |
| Free Resource Launcher     | Opens SimpleOptOut, JustDelete.me, and StopDataBrokers                     |
| Email Template Generator   | Builds privacy request drafts for brokers with email support               |
| Secure Personal Storage    | Uses `cryptography` (optional) to store identifiers in an encrypted file   |
| CSV-Driven Data Broker List| Customizable list of brokers with `covered_by` and `status` fields         |

---

## 🛠 Setup

```bash
pip install cryptography   # optional
python3 footprint_scrubber.py
```

The first time you run it, you'll be asked:
1. What paid services you use (Incogni, DeleteMe, etc.)
2. If you'd like to include free tools (SimpleOptOut, JustDelete.me, etc.)

---

## 📋 brokers.csv Format

```csv
name,url,email,notes,covered_by,status
Spokeo,https://www.spokeo.com/opt_out/new,,,Incogni;DeleteMe,Completed
```

- `covered_by`: Which services (semicolon-separated) already handle this broker
- `status`: Your progress (`Pending`, `Submitted`, `Completed`)

---

## 🧭 Menu Options

```
1. Collect & save personal data
2. Launch opt-out URLs (excluding paid-service coverage)
3. Generate email templates
4. Open free opt-out services
5. Re-run setup wizard
6. Manage services (add/remove paid or free tools)
7. Edit broker list (add brokers or update status)
8. Quit
```

---

## 💡 Tips

- Use Option 6 to update your service subscriptions at any time
- Use Option 7 to manage brokers without editing CSV manually
- Use Option 4 to access free resources that can supplement your opt-outs

---

© 2025 William “TwoWheelJunky” Peterson
