# Te Reo Hoa - Language Learning Backend API

🌟 **A comprehensive FastAPI backend for English-to-Māori language learning platform with PostgreSQL database**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)

---

## 📖 Overview

Te Reo Hoa is a modern, scalable backend API designed to power an English-to-Māori language learning platform. Built with **FastAPI** and **PostgreSQL**, it provides comprehensive features including user management, vocabulary learning, AI-powered translation, text-to-speech conversion, progress tracking, and curated news content.

### ✨ Key Features

- 🔐 **JWT Authentication** - Secure user authentication with role-based access control
- 🌐 **AI-Powered Translation** - Google Gemini integration for intelligent English-to-Māori translation
- 🔊 **Text-to-Speech** - AWS Polly integration for Māori pronunciation with intelligent caching
- 📚 **Vocabulary Management** - Comprehensive word database with learning progress tracking
- 📰 **Curated News** - Positive news content in both English and Māori
- 🎯 **Interactive Quizzes** - Assessment functionality for learning progress
- 📊 **Progress Tracking** - Detailed user learning analytics
- 🚀 **Auto-Provisioning** - Intelligent database setup with cross-platform compatibility
- 🗃️ **PostgreSQL Integration** - Production-grade database with Supabase cloud hosting
- 🧪 **Comprehensive Testing** - Advanced test suite with 9 specialized test modules

---

## 🚀 Latest Updates (July 2, 2025)

### Database Migration & Production Enhancement ✅
- **PostgreSQL Migration**: Successfully migrated to PostgreSQL for enhanced scalability and performance
- **Supabase Integration**: Cloud-based PostgreSQL database with secure authentication and backup
- **Dual Database Support**: PostgreSQL for production, SQLite for development environments
- **Enhanced Testing**: Comprehensive test suite with 9 specialized modules covering all functionality
- **Production Readiness**: Advanced database configuration for high-availability deployment

### Testing Infrastructure ✅
- **Comprehensive Test Coverage**: 9 specialized test modules including authentication, AI integration, and search functionality
- **Test Isolation**: Dedicated test database configuration preventing development data interference
- **Advanced Testing**: Mock handling for AI services and comprehensive endpoint validation
- **Quality Assurance**: Enhanced reliability through systematic testing of all major features

---

## 🚀 Previous Updates (June 30, 2025)

### Infrastructure Improvements ✅
- **Enhanced Database Configuration**: Robust SQLite setup with automatic directory creation
- **Cross-Platform Compatibility**: Consistent behavior across Windows, macOS, and Linux
- **Intelligent Error Handling**: Comprehensive database connection error recovery
- **Environment Configuration**: Streamlined setup with intelligent fallback systems
- **Login Endpoint Optimization**: Dual-path support resolving 307 redirect issues

### New Features ✅
- **TTS Caching System**: Intelligent audio file caching for improved performance
- **Enhanced AI Integration**: Extended timeout handling and improved response parsing
- **Auto-Provisioning**: Automatic creation of database directories and configuration files
- **Debug Integration**: Real-time database path and connection status reporting

---

## 🏗️ Architecture

### Project Structure

```
te-reo-hoa-backend/
├── 📱 app/                    # Main application package
│   ├── 🛣️ router/            # API endpoint organization
│   │   ├── login.py          # Authentication (dual-path support)
│   │   ├── users.py          # User management endpoints
│   │   ├── words.py          # Vocabulary management
│   │   ├── translate.py      # Translation services
│   │   ├── tts.py            # Text-to-Speech with caching
│   │   ├── progress.py       # Learning progress tracking
│   │   ├── quiz.py           # Assessment functionality
│   │   └── news.py           # News content delivery
│   ├── models.py             # SQLAlchemy database models
│   ├── schemas.py            # Pydantic validation schemas
│   ├── database.py           # Intelligent database configuration
│   ├── crud.py               # Database operation abstractions
│   ├── auth.py               # Authentication & authorization
│   ├── ai_integration.py     # External AI service integrations
│   └── utils.py              # Shared utility functions
├── 📊 data/                   # Database storage (environment-dependent)
│   ├── te_reo_hoa.db         # SQLite database file (development)
│   └── postgresql://         # PostgreSQL connection (production)
├── 🔊 static/                 # Static file serving
│   └── audio/                # Generated pronunciation files
│       └── tts_cache/        # Cached TTS audio files
├── ⚙️ config/                # Configuration files
│   └── settings.json         # Admin and application settings
├── 📚 docs/                   # Project documentation
│   ├── Architecture.md       # System architecture guide
│   └── Progress.md           # Development timeline
├── 🧪 tests/                  # Comprehensive test suite
│   ├── test_ai_function.py   # AI integration testing
│   ├── test_connection.py    # Database connectivity testing
│   ├── test_endpoint_auth.py # Authentication testing
│   ├── test_listing_words.py # Word listing functionality
│   ├── test_login.py         # Login system testing
│   ├── test_search_words.py  # Search functionality testing
│   ├── test_user_regsiter.py # User registration testing
│   ├── test_WOTD.py          # Word of the Day testing
│   └── conftest.py           # Test configuration
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### Technology Stack

- **Framework**: FastAPI (high-performance async web framework)
- **Database**: PostgreSQL with Supabase cloud hosting (production) / SQLite (development)
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI Services**: 
  - Google Gemini API (translation and content generation)
  - AWS Polly (Māori text-to-speech synthesis)
- **Validation**: Pydantic schemas for type safety
- **Scheduling**: APScheduler for background tasks
- **Testing**: Pytest with comprehensive coverage

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **pip** (Python package manager)
- **Virtual Environment** (recommended)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd te-reo-hoa-backend
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   # Database Configuration (Production)
   POSTGRE_SQLALCHEMY_DATABASE_URL=postgresql://username:password@host:port/database

   # Database Configuration (Development - Optional)
   SQLALCHEMY_DATABASE_URL=sqlite:///./data/te_reo_hoa.db

   # JWT Configuration
   SECRET_KEY=your-super-secret-jwt-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Google Gemini API
   GEMINI_API_KEY=your-google-gemini-api-key

   # AWS Configuration (for TTS)
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   AWS_REGION=us-east-1

   # News API (optional)
   NEWS_API_KEY=your-news-api-key
   ```

5. **Start the Application**
   ```bash
   # Development mode with auto-reload
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Production mode
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/

### 🔧 Configuration Notes

#### Database Setup
- **Production Database**: PostgreSQL on Supabase for scalable, cloud-based data management
- **Development Database**: SQLite with auto-provisioning for local development
- **Dual Configuration**: Supports both PostgreSQL and SQLite through environment variables
- **Migration Path**: Seamless migration from SQLite development to PostgreSQL production

#### Database Configuration Options
- **Primary (Production)**: Use `POSTGRE_SQLALCHEMY_DATABASE_URL` for PostgreSQL
- **Secondary (Development)**: Use `SQLALCHEMY_DATABASE_URL` for SQLite
- **Auto-Detection**: System automatically detects and uses the appropriate database configuration

#### Admin Account
- **Default Admin**: Automatically created on first startup
- **Configuration**: Modify `config/settings.json` to change default admin credentials
- **Security**: Change default password immediately in production

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/login/` | User authentication and token generation | ❌ |
| `POST` | `/users/register` | User registration | ❌ |
| `GET` | `/users/me` | Get current user profile | ✅ |

### Vocabulary Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/words/` | List all vocabulary words | ✅ |
| `POST` | `/words/add` | Add new vocabulary word | ✅ (Admin) |
| `PUT` | `/words/{word_id}` | Update existing word | ✅ (Admin) |
| `DELETE` | `/words/{word_id}` | Delete vocabulary word | ✅ (Admin) |

### Translation Services

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/translate/` | Translate English to Māori | ✅ |
| `POST` | `/translate/bulk` | Bulk translation of multiple texts | ✅ |

### Text-to-Speech (TTS)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/tts/tts` | Convert Māori text to speech | ❌ |
| `GET` | `/tts/audio/{cache_key}` | Direct access to cached audio files | ❌ |
| `GET` | `/tts/cache/info` | Get TTS cache information | ❌ |
| `DELETE` | `/tts/cache` | Clear TTS cache | ✅ (Admin) |

### Progress Tracking

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/progress/` | Get user learning progress | ✅ |
| `POST` | `/progress/update` | Update word learning status | ✅ |
| `GET` | `/progress/stats` | Get detailed progress statistics | ✅ |

### Quizzes & Assessment

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/quiz/generate` | Generate personalized quiz | ✅ |
| `POST` | `/quiz/submit` | Submit quiz answers | ✅ |
| `GET` | `/quiz/history` | Get quiz history | ✅ |

### News Content

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/news/` | Get curated positive news | ✅ |
| `GET` | `/news/{news_id}` | Get specific news article | ✅ |

---

## 🔐 Authentication & Security

### JWT Token Authentication
- **Algorithm**: HS256
- **Expiration**: Configurable (default: 30 minutes)
- **Refresh**: Automatic token refresh mechanism
- **Roles**: `admin` and `learner` role-based access control

### Security Features
- **Password Hashing**: Bcrypt with salt for secure password storage
- **CORS Protection**: Configurable CORS middleware for frontend integration
- **Input Validation**: Comprehensive Pydantic schema validation
- **SQL Injection Prevention**: SQLAlchemy ORM parameterization
- **Role-Based Access**: Granular permission control for different user types

### Usage Example
```bash
# Login to get token
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@admin.com&password=123456"

# Use token in subsequent requests
curl -X GET "http://localhost:8000/words/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🤖 AI Integration

### Google Gemini API
- **Translation**: Intelligent English-to-Māori translation with context awareness
- **Content Generation**: AI-powered content creation for learning materials
- **Extended Timeout**: 120-second timeout handling for complex requests
- **Response Parsing**: Intelligent JSON parsing with fallback mechanisms

### AWS Polly Text-to-Speech
- **Voice**: High-quality Māori pronunciation using Aria voice
- **Caching**: Intelligent audio file caching to reduce API costs
- **Formats**: MP3 audio output with configurable quality
- **Static Serving**: Direct audio file access through static file middleware

### Configuration
```env
# Required for AI features
GEMINI_API_KEY=your-google-gemini-api-key
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
```

---

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test modules
pytest tests/test_ai_function.py -v        # AI integration tests
pytest tests/test_connection.py -v        # Database connection tests
pytest tests/test_endpoint_auth.py -v     # Authentication tests
pytest tests/test_login.py -v             # Login functionality tests
pytest tests/test_search_words.py -v      # Search functionality tests
```

### Test Structure
- **Unit Tests**: Individual component testing across 9 specialized modules
- **Integration Tests**: API endpoint testing with authentication validation
- **Database Tests**: Connection and transaction testing for both PostgreSQL and SQLite
- **Authentication Tests**: Complete security mechanism verification
- **AI Integration Tests**: External service testing with mock responses
- **Search Tests**: Word search and discovery functionality validation

---

## 🚀 Deployment

### Development Deployment
```bash
# Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

#### Using Gunicorn
```bash
# Install Gunicorn
pip install gunicorn[standard]

# Start with multiple workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Using Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Environment Variables for Production
```env
# Production database (required)
POSTGRE_SQLALCHEMY_DATABASE_URL=postgresql://username:password@host:port/database

# Development database (optional)
SQLALCHEMY_DATABASE_URL=sqlite:///./data/te_reo_hoa.db

# Strong secret key
SECRET_KEY=your-strong-production-secret-key

# Production API keys
GEMINI_API_KEY=your-production-gemini-key
AWS_ACCESS_KEY_ID=your-production-aws-key
AWS_SECRET_ACCESS_KEY=your-production-aws-secret
```

---

## 📊 Performance & Monitoring

### Built-in Features
- **Comprehensive Logging**: Structured logging with file and console output
- **Database Connection Monitoring**: Real-time connection status and path validation
- **AI Service Monitoring**: Request/response tracking for external services
- **Performance Metrics**: Response time tracking and resource usage monitoring

### Monitoring Endpoints
- **Health Check**: `GET /` - Basic application health
- **Cache Info**: `GET /tts/cache/info` - TTS cache statistics
- **Database Status**: Built-in database connection monitoring

### Log Files
- **Application Logs**: `app.log` (in project root)
- **Error Tracking**: Comprehensive error logging with stack traces
- **Performance Logs**: Request timing and resource usage

---

## 🛠️ Development

### Code Quality
- **Formatting**: Black code formatter
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **Error Handling**: Comprehensive exception handling with meaningful messages

### Development Tools
```bash
# Code formatting
black .

# Type checking
mypy app/

# Linting
flake8 app/

# Security scanning
bandit -r app/
```

### Contributing Guidelines
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Write tests** for new functionality
4. **Format code**: `black .`
5. **Run tests**: `pytest`
6. **Submit pull request**

---

## 📋 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Error: unable to open database file
# Solution: Check database path and permissions
```
- **Auto-Fix**: The application automatically creates missing directories
- **Manual Fix**: Ensure `/data` directory exists with write permissions
- **Debug**: Check logs for database path resolution details

#### TTS Cache Issues
```bash
# Error: Failed to generate audio
# Solution: Check AWS credentials and cache directory
```
- **Cache Clear**: Use `DELETE /tts/cache` endpoint (admin required)
- **Directory Check**: Ensure `./static/audio/tts_cache/` exists
- **AWS Config**: Verify AWS credentials and region settings

#### Authentication Problems
```bash
# Error: 401 Unauthorized
# Solution: Check JWT token and expiration
```
- **Token Refresh**: Re-authenticate to get new token
- **Admin Access**: Ensure user has appropriate role
- **Secret Key**: Verify SECRET_KEY environment variable

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn main:app --reload --log-level debug
```

---

## 📞 Support & Contact

### Documentation
- **Architecture Guide**: [`docs/Architecture.md`](docs/Architecture.md)
- **Development Progress**: [`docs/Progress.md`](docs/Progress.md)
- **API Documentation**: http://localhost:8000/docs (when running)

### Support Channels
- **Issues**: GitHub Issues for bug reports and feature requests
- **Development**: Check `docs/Progress.md` for current development status
- **Configuration**: Refer to this README for setup and configuration guidance

---

## 📄 License

This project is part of the MSE800 Post School Education program at YooBee Colleges.

---

## 🔄 Changelog

### Version 1.0 (June 30, 2025)
- ✅ **Infrastructure Improvements**: Enhanced database configuration and auto-provisioning
- ✅ **TTS Integration**: Complete text-to-speech functionality with intelligent caching
- ✅ **Cross-Platform Support**: Consistent behavior across Windows, macOS, and Linux
- ✅ **Enhanced Documentation**: Comprehensive architecture and setup documentation
- ✅ **Error Handling**: Robust error recovery and debugging capabilities
- ✅ **Login Optimization**: Dual-path endpoint support for better compatibility

### Previous Versions
- **v0.9**: Core API functionality with basic authentication
- **v0.8**: AI integration with Google Gemini and AWS Polly
- **v0.7**: Database models and CRUD operations
- **v0.6**: Initial FastAPI setup and project structure

---

*Last Updated: June 30, 2025*  
*Status: Production Ready with Enhanced Infrastructure*
