# Te Reo Hoa Backend API

Te Reo Hoa is a comprehensive language learning web application that helps users engage with and learn Te Reo Māori. The backend provides a robust FastAPI-based REST API with AI-powered translation, user progress tracking, vocabulary management, and curated news content.

---

## 🌟 Features

### Authentication & User Management
- JWT-based authentication with OAuth2
- Role-based access control (admin, staff, learner)
- User registration and profile management
- Admin user promotion capabilities

### Vocabulary & Translation
- AI-powered English-to-Māori translation (Google Gemini API)
- Comprehensive word/phrase database with metadata
- Audio pronunciation generation (AWS Polly)
- Word categorization by level, type, and domain
- Duplicate detection and normalization
- Example sentences and cultural notes

### Learning & Progress Tracking
- User progress tracking (learned, review, starred, unlearned)
- Personal vocabulary statistics
- Interactive quiz system with multiple-choice questions
- Word-of-the-day functionality

### Content & News
- Curated positive Māori news feed
- AI-filtered uplifting stories
- News source integration with image support
- Automatically fetch news every 3am daily
- Manual news fetch by admin

### Technical Features
- CORS-ready API for frontend integration
- Robust error handling and validation
- Modular router-based architecture
- SQLite database with SQLAlchemy ORM
- Comprehensive test coverage

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI 
- **Database:** SQLite (development), PostgreSQL-ready (production)
- **ORM:** SQLAlchemy with Alembic migrations
- **Authentication:** OAuth2 with JWT tokens
- **AI Integration:** Google Gemini API for translation and content filtering
- **Audio:** AWS Polly for Text-to-Speech
- **Testing:** Pytest
- **Development Server:** Uvicorn
- **Frontend:** Next.js (separate repository)

---

## � Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- API keys for Google Gemini and AWS Polly

### Setup Instructions

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd te-reo-hoa-backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux  
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Database Setup**
   ```bash
   # Database tables are auto-created on first run
   python -c "from app.database import engine; from app import models; models.Base.metadata.create_all(bind=engine)"
   ```

6. **Start Development Server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## 📁 Project Structure

```
te-reo-hoa-backend/
├── app/
│   ├── router/          # API route modules
│   │   ├── users.py     # User management
│   │   ├── words.py     # Vocabulary management  
│   │   ├── progress.py  # Learning progress
│   │   ├── quiz.py      # Quiz functionality
│   │   ├── translate.py # Translation service
│   │   ├── login.py     # Authentication
│   │   └── news.py      # News feed
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # Database configuration
│   ├── crud.py          # Database operations
│   ├── auth.py          # Authentication logic
│   ├── ai_integration.py # AI service integrations
│   └── utils.py         # Utility functions
├── tests/               # Test suite
├── static/              # Static files (audio, etc.)
├── docs/                # Documentation
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🔧 Configuration

### Required Environment Variables
```env
# AI Services
GEMINI_API_KEY=your_gemini_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Authentication
SECRET_KEY=your_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./te_reo_hoa.db
```

---

## 📚 Documentation

- [Architecture Overview](./docs/Architecture.md) - System design and component details
- [Progress Log](./docs/Progress.md) - Development updates and milestones
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI (when running)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_basic.py -v
```

---

## 🌐 Deployment

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# Using Gunicorn (recommended)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or direct Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Support
```dockerfile
# Basic Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Roadmap

- [ ] Enhanced quiz types (translation, audio recognition)
- [ ] Spaced repetition algorithm
- [ ] Advanced progress analytics  
- [ ] Mobile app integration
- [ ] Community features (user-generated content)
- [ ] Offline functionality support
- [ ] Multi-dialect Māori support