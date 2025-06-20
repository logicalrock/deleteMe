from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import users
from app import config
import os

# App instance
app = FastAPI(
    title=f"{config.APP_NAME} by {config.APP_AUTHOR}",
    debug=config.DEBUG
)

# Mount static directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=templates_dir)

# Include your routers
app.include_router(users.router)

