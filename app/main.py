from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import SessionLocal, engine
from . import models, schemas, auth, crud
from . import ai_integration
from .utils import sanitize_ai_data, extract_json_from_markdown, extract_ai_text

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Te Reo Hoa API")

# Allowed origins (frontend URLs)
origins = [
    "http://localhost:3000",    # For local frontend dev (React, etc.)
    "https://te-reo-hoa.vercel.com"   # Your deployed frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Specific origins
    allow_credentials=True,
    # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    allow_headers=["*"]               # Allow all headers
)

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Te Reo Hoa Backend(API) is running"}


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# Admin-only: List all users


@app.get("/users/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_user=Depends(auth.require_admin)):
    return crud.get_users(db)


@app.post("/users/{user_id}/set_admin", response_model=schemas.UserOut)
def set_admin(user_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_admin_user)):
    # Only admins can call this
    user = crud.set_user_role(db, user_id, "admin")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/words/", response_model=list[schemas.WordOut])
def list_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_words(db, skip=skip, limit=limit)


# @app.post("/words/", response_model=schemas.WordOut)
# def create_word(word: schemas.WordCreate, db: Session = Depends(get_db)):
#    normalized = word.text.strip().lower()
#    db_word = crud.get_word_by_normalized(db, normalized)
#    if db_word:
#        raise HTTPException(status_code=400, detail="Word already exists")
#    return crud.create_word(db, word, ai_data)


@app.post("/words/", response_model=schemas.WordOut)
async def add_word(
    word: schemas.WordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.require_admin)
):
    normalized = word.text.strip().lower()
    if crud.get_word_by_normalized(db, normalized):
        raise HTTPException(status_code=400, detail="Text already exists")
    # --- Call Gemini ---
    result = await ai_integration.get_translation(word.text)
    raw_ai_text = extract_ai_text(result)
    if not raw_ai_text:
        print("AI full response:", result)  # For debugging
        raise HTTPException(
            status_code=502, detail="AI did not return a usable response.")
    # --- Parse/clean AI output ---
    try:
        ai_data = extract_json_from_markdown(raw_ai_text)
        ai_data = sanitize_ai_data(ai_data)
    except Exception as e:
        print("Failed to parse AI response:", e)
        print("Raw text:", raw_ai_text)
        raise HTTPException(
            status_code=502, detail="Failed to parse AI response.")
    # --- Store to DB ---
    return crud.create_word(db, word.text, ai_data)

# Only admin can edit a word


@app.put("/words/{word_id}", response_model=schemas.WordOut)
def update_word(word_id: int, word: schemas.WordCreate, db: Session = Depends(get_db), current_user=Depends(auth.require_admin)):
    db_word = db.query(models.Word).get(word_id)
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    # Similar logic as create; you can also re-run AI here if desired
    db_word.text = word.text
    # (update other fields as needed)
    db.commit()
    db.refresh(db_word)
    return db_word
