from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import models, auth
from app.database import engine, SessionLocal
from app.router import login, news, progress, quiz, translate, tts, users, words
from app.utils import start_scheduler

import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for even more detail
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        # Logs to a file in your project root
        logging.FileHandler("app.log"),
        logging.StreamHandler()             # Also logs to your terminal/console
    ]
)

logger = logging.getLogger(__name__)


def load_default_admin_config():
    """Load default admin configuration from config/settings.json."""
    config_path = "config/settings.json"
    try:
        if not os.path.exists(config_path):
            logger.warning(f"Config file {config_path} not found, using fallback admin settings")
            return {"email": "admin@admin.com", "password": "123456"}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        default_admin = config.get("default_admin", {})
        if not default_admin.get("email") or not default_admin.get("password"):
            logger.warning("Invalid admin config in settings.json, using fallback settings")
            return {"email": "admin@admin.com", "password": "123456"}
        
        return default_admin
    except Exception as e:
        logger.error(f"Error loading admin config from {config_path}: {e}")
        return {"email": "admin@admin.com", "password": "123456"}


def init_default_admin():
    """Initialize default admin account if it doesn't exist."""
    db = SessionLocal()
    try:
        # Load admin config from settings.json
        admin_config = load_default_admin_config()
        admin_email = admin_config["email"]
        admin_password = admin_config["password"]
        
        # Check if the specific admin account exists
        existing_user = auth.get_user_by_email(db, admin_email)
        
        if existing_user:
            # If user exists but is not admin, promote to admin
            if existing_user.role != "admin":
                existing_user.role = "admin"
                db.commit()
                logger.info(f"Promoted existing user {admin_email} to admin role")
            else:
                logger.info(f"Admin account {admin_email} already exists with admin role")
        else:
            # Create new admin account
            hashed_password = auth.get_password_hash(admin_password)
            admin_user = models.User(
                email=admin_email,
                hashed_password=hashed_password,
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            logger.info(f"Created default admin account: {admin_email}")
            
    except Exception as e:
        logger.error(f"Error creating default admin account: {e}")
        db.rollback()
    finally:
        db.close() 


# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize default admin account
init_default_admin()

app = FastAPI(title="Te Reo Hoa API")

origins = ["http://localhost:3000",
           "https://te-reo-hoa.vercel.app",
           "http://localhost:62674"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Te Reo Hoa Backend(API) is running"}


start_scheduler()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(login.router, prefix="/login")
app.include_router(users.router, prefix="/users")
app.include_router(words.router, prefix="/words")
app.include_router(translate.router, prefix="/translate")
app.include_router(progress.router, prefix="/progress")
app.include_router(quiz.router, prefix="/quiz")
app.include_router(news.router, prefix="/news")
app.include_router(tts.router, prefix="/tts")
