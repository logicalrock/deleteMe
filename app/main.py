from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/start")
async def start_session(username: str = Form(...)):
    # Future: Load user profile here
    return RedirectResponse(url=f"/welcome/{username}", status_code=303)

@app.get("/welcome/{username}", response_class=HTMLResponse)
async def welcome_user(username: str, request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "username": username,
        "message": f"Welcome back, {username}! We're preparing your data scrub session."
    })

