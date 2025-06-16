from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.router import users, words, progress, quiz, translate, login, news

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Te Reo Hoa API")

origins = [
    "http://localhost:3000",
    "https://te-reo-hoa.vercel.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"message": "Te Reo Hoa Backend(API) is running"}


app.include_router(login.router, prefix="/login")
app.include_router(users.router, prefix="/users")
app.include_router(words.router, prefix="/words")
app.include_router(translate.router, prefix="/translate")
app.include_router(progress.router, prefix="/progress")
app.include_router(quiz.router, prefix="/quiz")
app.include_router(news.router, prefix="/news")
