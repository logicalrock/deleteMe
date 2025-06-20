<<<<<<< HEAD
# deleteMe

**deleteMe** is a Python-based digital footprint scrubbing toolkit that helps users remove personal data from online data brokers.  
It evolved over four versions, adding service integration, automation, and usability improvements.

---------------------------------------------------------------------------------------------------------------------------------|||||

# deleteMe Project

## Versions
- 🔹 [deleteMe CLI version](./deleteMe_v4/README.md)
- 🔸 [deleteMe Web version](./deleteMeWeb/README.md)

---------------------------------------------------------------------------------------------------------------------------------|||||

# Version Summary

| Folder         | Description                                               |
|----------------|-----------------------------------------------------------|
| `deleteMe_v1/` | Initial working concept: identifier collection and link output |
| `deleteMe_v2/` | Added CSV-driven broker list, secure storage, email generator |
| `deleteMe_v3/` | Integrated paid service awareness (Incogni, DeleteMe, etc.) |
| `deleteMe_v4/` | CLI-based Broker Editor, auto-matching covered brokers, refined UX |

Each folder is self-contained with:
- `deleteMe.py` – the main Python program
- `README.md` – usage info specific to the version
- `VERSION.txt` – version number and release date
- `brokers.csv` – editable list of broker info

---------------------------------------------------------------------------------------------------------------------------------|||||

# Quick Start (v4)

```bash
cd deleteMe_v4
python3 deleteMe.py
```

The CLI will guide you through:
1. Entering personal data (e.g., email, phone numbers, usernames)
2. Selecting any paid or free services you already use (Incogni, DeleteMe, etc.)
3. Automatically identifying which brokers are already covered
4. Launching opt-out URLs or generating custom email templates
5. Editing or adding brokers from the CLI in real time

---------------------------------------------------------------------------------------------------------------------------------|||||

# Python Packaging (v4 only)

To install as a CLI tool:

```bash
cd deleteMe_v4
pip install .
```

This exposes a global command:

```bash
deleteMe
```

---------------------------------------------------------------------------------------------------------------------------------|||||

# Documentation Files

| File             | Purpose                                      |
|------------------|----------------------------------------------|
| `README.md`      | This file – describes repo structure and usage |
| `CHANGELOG.md`   | Summarizes new features by version           |
| `.gitignore`     | Ensures backups, bytecode, and tools are excluded |
| `VERSION.txt`    | Located inside each version folder, holds version info |

---------------------------------------------------------------------------------------------------------------------------------|||||

# Future Plans

- Integration with browser automation (Selenium, Playwright)
- Plugin system for other paid services
- GUI-based wrapper for non-technical users

---------------------------------------------------------------------------------------------------------------------------------|||||

# Author

William “TwoWheelJunky” Peterson  
GitHub: [logicalrock](https://github.com/logicalrock)

(c) 2025 All rights reserved.
=======
# deleteMe Web — by DarkVeil Security

**deleteMe Web** is a modern web interface for managing your personal data opt-outs across hundreds of data broker websites. Built using FastAPI and Jinja2, it extends the command-line power of `deleteMe` with an accessible, intuitive interface for multiple users and household use.

---

# Project Philosophy

**"deleteMe" is a quiet digital resistance tool.**  
It doesn't broadcast. It doesn't sell.  
It just helps you vanish.

Built by **DarkVeil Security** — defenders in the shadows.

---

# Folder Structure

```
deleteMeWeb/
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── routers/               # API route files (users, brokers, etc.)
│   ├── templates/             # HTML templates (Jinja2)
│   │   └── home.html
│   ├── static/                # CSS, logos, JS
│   │   └── style.css
├── darkVeil_007_BlackLetters_NoBackground.png
├── README.md                  # ← You are here
├── requirements.txt           # Project dependencies
└── venv/                      # Python virtual environment (excluded by .gitignore)
```

---

# Getting Started

# 1. Clone the project

```bash
git clone https://github.com/logicalrock/deleteMe.git
cd deleteMe/deleteMeWeb
```

# 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

# 3. Environment Variables

Copy `.env.example` and rename to `.env`:

```bash
cp .env.example .env

# 4. Install dependencies

```bash
pip install -r requirements.txt
```

> Make sure to include `jinja2`, `fastapi`, `uvicorn`, `python-multipart`, `pydantic`, and `platformdirs` in your `requirements.txt`.

---

# Running the App (Development Mode)

```bash
uvicorn app.main:app --reload
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
View API docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# Custom Branding

This version includes DarkVeil Security branding and supports your personal logo:

- **Logo file:** `darkVeil_007_BlackLetters_NoBackground.png`
- Auto-included in `home.html`
- CSS stylings are handled in `static/style.css`

Feel free to swap or reposition it in `templates/home.html`.

---

# Multi-User Support

Each user has a separate profile saved to:

```
~/.local/share/deleteMeWeb/users/
```

Returning users will be greeted and offered to resume where they left off.

---

# Coming Soon

- ✅ Personal data CSV import
- 🟡 Broker opt-out API automation
- 🟡 OAuth account linking (DeleteMe, Incogni, etc.)
- 🔒 Encrypted user sessions
- 🧑‍💻 Admin-only reporting panel

---

# 🕶️ Built by DarkVeil Security

We don’t podcast.  
We don’t tweet.  
We delete.

https://www.darkveilsecurity.com
>>>>>>> 2fb26e1 (Initial commit after move)
