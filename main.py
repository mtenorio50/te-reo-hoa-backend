from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import models
from app.database import engine
from app.router import login, news, progress, quiz, translate, users, words
from app.utils import start_scheduler

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

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Te Reo Hoa API")

origins = ["http://localhost:3000", "https://te-reo-hoa.vercel.com", 'http://localhost:62674']

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
