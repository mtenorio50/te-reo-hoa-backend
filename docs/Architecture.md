# Te Reo Hoa Project Architecture

## Overview

Te Reo Hoa is a language learning platform focused on English-to-Māori translation, word/phrase management, user progress tracking, and AI-powered content. The project uses a modular, scalable backend and is ready for integration with various frontends.

---

## System Components

### 1. **Frontend**
- (Planned or in progress)
- User authentication and dashboard
- Word lookup and translation display
- Progress tracking UI
- Daily word and notification panel

### 2. **Backend API (FastAPI)**
- Handles all business logic and database operations
- Exposes REST endpoints for:
    - User registration & login (OAuth2)
    - Word/phrase management (CRUD)
    - Translation via AI integration
    - User progress (learned, to review, starred, unlearned)
    - Daily word endpoint

### 3. **Database (SQLite)**
- Stores users, words, translations, user progress, logs, etc.
- ORM: SQLAlchemy

#### **Key Tables:**
- `users`: User authentication and profiles
- `words`: Word/Phrase records, level (basic/intermediate), domains
- `translations`: English↔Māori mappings, usage examples, notes, type
- `progress`: User-specific word learning status
- `logs`: Audit trails (optional)

### 4. **AI Integration**
- Connects to language model (e.g., OpenAI) for automated translation and suggestions
- Extracts sentence usage, type, and notes from AI response

### 5. **Authentication & Authorization**
- OAuth2 with token-based authentication
- Role management (Admin, Staff, User)

### 6. **Utilities**
- Input sanitation (trimming, case normalization)
- Error handling and logging

### 7. **CORS Middleware**
- Configured for secure frontend-backend communication

---
[ User / Frontend ]
|
v
[ FastAPI Backend ]
| | |
v v v
[Database] [AI Service] [Auth/CORS]


- **User/Frontend:** Sends requests to FastAPI backend.
- **FastAPI Backend:** Orchestrates requests, enforces logic, calls AI service, manages DB.
- **Database:** Stores persistent data.
- **AI Service:** Provides translations and language enrichment.
- **Auth/CORS:** Secures endpoints and allows frontend requests.

---
app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── auth.py
├── ai_integration.py
├── utils.py
├── routers/
│ └── (optional route files)
└── tests/
└── test_*.py

---

## Deployment Notes

- **Backend:** FastAPI, Uvicorn
- **Database:** SQLite (dev), scalable to Postgres (prod)
- **Frontend:** React/Vue/Other (planned)
- **Environment:** Docker support recommended

---

## Notes

- Strict role-based permissions for admin endpoints
- All AI integration (translation, news positivity) is performed server-side for privacy and caching
- Designed for easy extension: new news sources, more quiz types, or more granular progress tracking


