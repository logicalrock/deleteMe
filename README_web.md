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

# 3. Install dependencies

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
