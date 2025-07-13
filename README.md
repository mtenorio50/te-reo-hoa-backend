# Te Reo Hoa - Language Learning Backend API

🌟 **A comprehensive FastAPI backend for English-to-Māori language learning platform with PostgreSQL database**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
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
- 🧪 **Comprehensive Testing** - Advanced test suite with 14 specialized test modules

---

## 📋 **Complete Setup Checklist for New Machine**

This guide covers everything needed to run Te Reo Hoa on a fresh machine, from system requirements to full deployment.

---

## 🔧 **System Requirements**

### **Essential Software**
- ✅ **Python 3.8+** (3.9+ recommended)
- ✅ **pip** (Python package manager)
- ✅ **Git** (for cloning repository)
- ✅ **Virtual Environment** (venv or conda)

### **Optional but Recommended**
- ✅ **VS Code** or **PyCharm** (IDE)
- ✅ **PostgreSQL Client** (for database management)
- ✅ **Postman** or **Thunder Client** (API testing)

---

## 📦 **Step-by-Step Installation**

### **Step 1: Install Python & Dependencies**

#### **Windows:**
```powershell
# Download Python from python.org (3.9+)
# Or use Windows Store
winget install Python.Python.3.9

# Verify installation
python --version
pip --version
```

#### **macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.9

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### **Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3.9 python3.9-venv python3-pip

# Verify installation
python3 --version
pip3 --version
```

### **Step 2: Clone the Repository**

```bash
# Clone from GitHub
git clone https://github.com/mtenorio50/te-reo-hoa-backend.git
cd te-reo-hoa-backend

# Or extract from submission ZIP
# Extract Te_Reo_Hoa_FullStack_Submission.zip
# Navigate to backend/ folder
```

### **Step 3: Create Virtual Environment**

#### **Windows:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show (venv) in prompt)
```

#### **macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) in prompt)
```

### **Step 4: Install Project Dependencies**

```bash
# Ensure virtual environment is activated
# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list
```

### **Step 5: Environment Configuration**

#### **Create .env File**
Create a `.env` file in the project root with the following configuration:

```env
# ==========================================
# DATABASE CONFIGURATION (REQUIRED)
# ==========================================
# PostgreSQL connection string for Supabase
POSTGRE_SQLALCHEMY_DATABASE_URL=postgresql://username:password@host:port/database

# Example for Supabase:
# POSTGRE_SQLALCHEMY_DATABASE_URL=postgresql://postgres.xxxxxxxxxxxx:your_password@aws-0-region.pooler.supabase.com:5432/postgres

# ==========================================
# JWT AUTHENTICATION (REQUIRED)
# ==========================================
SECRET_KEY=your-super-secret-jwt-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ==========================================
# AI SERVICES (REQUIRED FOR FULL FUNCTIONALITY)
# ==========================================
# Google Gemini API for translation
GEMINI_API_KEY=your-google-gemini-api-key

# AWS Configuration for Text-to-Speech
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

# ==========================================
# OPTIONAL SERVICES
# ==========================================
# News API (optional - for news features)
NEWS_API_KEY=your-news-api-key

# ==========================================
# APPLICATION SETTINGS
# ==========================================
# Environment
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO

# CORS (if needed for frontend)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 🗃️ **Database Setup**

### **Option 1: Supabase (Recommended)**

1. **Create Supabase Account**
   - Go to [supabase.com](https://supabase.com)
   - Create free account
   - Create new project

2. **Get Connection String**
   - Navigate to Settings → Database
   - Copy PostgreSQL connection string
   - Add to `.env` as `POSTGRE_SQLALCHEMY_DATABASE_URL`

3. **Database Initialization**
   ```bash
   # The application will automatically create tables on first run
   python main.py
   ```

### **Option 2: Local PostgreSQL**

1. **Install PostgreSQL**
   ```bash
   # Windows (using Chocolatey)
   choco install postgresql

   # macOS (using Homebrew)
   brew install postgresql

   # Linux (Ubuntu/Debian)
   sudo apt install postgresql postgresql-contrib
   ```

2. **Create Database**
   ```sql
   -- Connect to PostgreSQL
   psql -U postgres

   -- Create database
   CREATE DATABASE te_reo_hoa;

   -- Create user (optional)
   CREATE USER te_reo_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE te_reo_hoa TO te_reo_user;
   ```

3. **Update .env**
   ```env
   POSTGRE_SQLALCHEMY_DATABASE_URL=postgresql://te_reo_user:your_password@localhost:5432/te_reo_hoa
   ```

---

## 🔑 **API Keys Setup**

### **Google Gemini API**

1. **Get API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create new API key
   - Add to `.env` as `GEMINI_API_KEY`

2. **Enable Required APIs**
   - Ensure Gemini API is enabled in your Google Cloud Console

### **AWS Polly (Text-to-Speech)**

1. **Create AWS Account**
   - Sign up at [aws.amazon.com](https://aws.amazon.com)
   - Navigate to IAM service

2. **Create IAM User**
   - Create user with Polly permissions
   - Generate access keys
   - Add keys to `.env`

3. **Required Permissions**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "polly:SynthesizeSpeech",
           "polly:DescribeVoices"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

---

## 🚀 **Running the Application**

### **Development Mode**
```bash
# Ensure virtual environment is activated
# Start with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Production Mode**
```bash
# Start without auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000

# Or using Gunicorn (install first: pip install gunicorn)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Verify Installation**
1. **Check Application Status**
   - Open browser to: http://localhost:8000
   - Should see: `{"message": "Te Reo Hoa API is running!"}`

2. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test Health Endpoint**
   - Health Check: http://localhost:8000/health

---

## 🧪 **Testing the Setup**

### **Run Test Suite**
```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test categories
pytest tests/test_connection.py -v    # Database connection
pytest tests/test_endpoint_auth.py -v # Authentication
pytest tests/test_ai_function.py -v   # AI integration (requires API keys)
```

### **Manual API Testing**

1. **Test Registration**
   ```bash
   curl -X POST "http://localhost:8000/users/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "testpass123", "role": "learner"}'
   ```

2. **Test Login**
   ```bash
   curl -X POST "http://localhost:8000/login/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@admin.com&password=123456"
   ```

3. **Test Protected Endpoint**
   ```bash
   # Use token from login response
   curl -X GET "http://localhost:8000/words/" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

---

## 📁 **Directory Structure After Setup**

```
te-reo-hoa-backend/
├── venv/                      # Virtual environment (created)
├── .env                       # Environment variables (created)
├── app.log                    # Application logs (auto-created)
├── static/                    # Static files directory
│   └── audio/                 # TTS audio cache (auto-created)
├── config/
│   └── settings.json          # Admin settings (auto-created)
├── app/                       # Application source code
├── tests/                     # Test suite
├── docs/                      # Documentation
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies
└── README.md                  # This documentation
```

---

## ⚠️ **Common Issues & Solutions**

### **Issue: Python Version Errors**
```bash
# Error: Python version too old
# Solution: Install Python 3.8+
python --version  # Check current version
```

### **Issue: Module Not Found Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### **Issue: Database Connection Failed**
```bash
# Error: Database connection failed
# Solutions:
# 1. Check .env file has correct DATABASE_URL
# 2. Verify database credentials
# 3. Ensure database server is running
# 4. Check network connectivity
```

### **Issue: Permission Denied (Windows)**
```powershell
# Error: Execution policy prevents script running
# Solution: Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Issue: Port Already in Use**
```bash
# Error: Port 8000 already in use
# Solution: Use different port
uvicorn main:app --reload --port 8001

# Or kill existing process
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -ti:8000 | xargs kill
```

### **Issue: AI API Errors**
```bash
# Error: AI service failures
# Solutions:
# 1. Verify API keys in .env
# 2. Check API quotas/billing
# 3. Test with minimal requests
# 4. Check network connectivity
```

---

## 🔐 **Security Considerations**

### **Production Setup**
1. **Change Default Credentials**
   - Update admin password from default (123456)
   - Use strong JWT secret key

2. **Environment Variables**
   - Never commit .env file to version control
   - Use strong, unique passwords
   - Rotate API keys regularly

3. **Database Security**
   - Use SSL connections for database
   - Implement proper firewall rules
   - Regular security updates

4. **Server Configuration**
   - Use HTTPS in production
   - Configure proper CORS origins
   - Enable rate limiting

---

## 🚀 **Deployment Options**

### **Option 1: Local Development**
- Follow steps above
- Use for development and testing

### **Option 2: Cloud Deployment (Render.com)**
1. **Connect GitHub Repository**
2. **Set Environment Variables** in Render dashboard
3. **Deploy** - automatic from main branch

### **Option 3: Docker Deployment**
```dockerfile
# Dockerfile included in project
docker build -t te-reo-hoa .
docker run -p 8000:8000 --env-file .env te-reo-hoa
```

---

## 📞 **Getting Help**

### **Documentation**
- **README.md**: Main setup guide (this file)
- **Architecture.md**: System architecture details
- **Progress.md**: Development timeline
- **API Docs**: http://localhost:8000/docs (when running)

### **Common Commands Reference**
```bash
# Virtual environment
python -m venv venv              # Create
source venv/bin/activate         # Activate (macOS/Linux)
venv\Scripts\activate            # Activate (Windows)
deactivate                       # Deactivate

# Dependencies
pip install -r requirements.txt  # Install all
pip freeze > requirements.txt    # Update requirements
pip list                         # Show installed packages

# Application
python main.py                   # Run application
pytest                          # Run tests
uvicorn main:app --reload       # Run with auto-reload
```

---

**🎉 Once all steps are completed, you'll have a fully functional Te Reo Hoa backend running on your new machine!**

## 🚀 Latest Updates (July 12, 2025)

### Enhanced Documentation & Testing Infrastructure ✅
- **Advanced Testing Framework**: 14 specialized test modules covering all critical functionality areas
- **Audio Processing Enhancement**: Added TTS audio synthesis testing with comprehensive audio validation
- **IPA Phonetic Integration**: Enhanced phonetic transcription support for accurate pronunciation
- **Production Deployment Ready**: Render.com deployment configuration with health monitoring

### System Architecture Improvements ✅
- **Router-Based Architecture**: Modular endpoint organization with dedicated router modules
- **Enhanced Error Handling**: Comprehensive exception management across all API endpoints
- **Static File Management**: Optimized static file serving for audio and media assets
- **Configuration Management**: JSON-based settings with environment-specific configurations
- **Health Monitoring**: Dedicated health check endpoints for deployment monitoring

---

## 🚀 Previous Updates (June 30, 2025)

### Infrastructure Improvements ✅
- **Enhanced Database Configuration**: Robust PostgreSQL setup with automatic connection management
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
│   │   ├── login.py          # Authentication endpoints
│   │   ├── users.py          # User management endpoints
│   │   ├── words.py          # Vocabulary management
│   │   ├── translate.py      # Translation services
│   │   ├── tts.py            # Text-to-Speech with caching
│   │   ├── progress.py       # Learning progress tracking
│   │   ├── quiz.py           # Assessment functionality
│   │   └── news.py           # News content delivery
│   ├── models.py             # SQLAlchemy database models
│   ├── schemas.py            # Pydantic validation schemas
│   ├── database.py           # Database configuration & connection
│   ├── db_initialize.py      # Database initialization utilities
│   ├── crud.py               # Database operation abstractions
│   ├── auth.py               # Authentication & authorization
│   ├── ai_integration.py     # External AI service integrations
│   └── utils.py              # Shared utility functions
├── 📊 static/                 # Static file serving
│   └── audio/                # Audio file management
│       └── tts_cache/        # Cached TTS audio files
├── ⚙️ config/                # Configuration files
│   └── settings.json         # Admin and application settings
├── 📚 docs/                   # Project documentation
│   ├── Architecture.md       # System architecture guide
│   ├── Progress.md           # Development timeline
├── 🧪 tests/                  # Comprehensive test suite (14 modules)
│   ├── test_ai_function.py   # AI integration testing
│   ├── test_api_*.py         # API endpoint testing (news, progress, users, words)
│   ├── test_audio_synthesis.py # TTS audio processing testing
│   ├── test_connection.py    # Database connectivity testing
│   ├── test_endpoint_auth.py # Authentication testing
│   ├── test_ipa_phonetic.py  # IPA phonetic transcription testing
│   ├── test_listing_words.py # Word listing functionality
│   ├── test_login.py         # Login system testing
│   ├── test_search_words.py  # Search functionality testing
│   ├── test_user_regsiter.py # User registration testing
│   ├── test_WOTD.py          # Word of the Day testing
│   ├── ipa.py                # IPA phonetic utilities
│   └── conftest.py           # Test configuration and fixtures
├── .github/                  # GitHub Actions and workflows
├── main.py                   # Application entry point with scheduler
├── requirements.txt          # Python dependencies (100+ packages)
├── .env                      # Environment configuration
├── app.log                   # Application logging
└── README.md                 # This documentation
```

### Technology Stack

- **Framework**: FastAPI (high-performance async web framework)
- **Database**: PostgreSQL with Supabase cloud hosting
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI Services**: 
  - Google Gemini API (translation and content generation)
  - AWS Polly (Māori text-to-speech synthesis)
- **Audio Processing**: TTS synthesis with intelligent caching system
- **Validation**: Pydantic schemas for comprehensive type safety
- **Scheduling**: APScheduler for background tasks and automation
- **Testing**: Pytest with 14 specialized test modules for comprehensive coverage
- **Deployment**: Render.com compatible with health monitoring
- **Logging**: Structured logging with file and console output
- **Static Files**: FastAPI StaticFiles for efficient media serving

---

### 🔧 Configuration Notes

#### Database Setup
- **Production Database**: PostgreSQL on Supabase for scalable, cloud-based data management
- **Configuration**: Uses `POSTGRE_SQLALCHEMY_DATABASE_URL` environment variable
- **Connection**: Automatic connection pooling and session management

#### Database Configuration Options
- **Primary**: Uses `POSTGRE_SQLALCHEMY_DATABASE_URL` for PostgreSQL connection
- **Auto-Detection**: System automatically validates database connection on startup

#### Admin Account
- **Default Admin**: Automatically created on first startup from `config/settings.json`
- **Configuration**: Modify `config/settings.json` to change default admin credentials
- **Fallback Credentials**: admin@admin.com/123456 (if config file missing)
- **Auto-Promotion**: Existing users are automatically promoted to admin role if needed
- **Security**: Change default password immediately in production environments

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
| `GET` | `/news/` | Get latest 10 positive news stories | ❌ |
| `GET` | `/news/all` | Get paginated list of all news stories | ✅ (Admin) |
| `POST` | `/news/refresh` | Refresh news from Gemini AI | ✅ (Admin) |
| `POST` | `/news/refresh/manual` | Manually trigger news refresh | ✅ (Admin) |
| `GET` | `/news/scheduler-status` | Check news scheduler status | ✅ (Admin) |
| `DELETE` | `/news/{news_id}` | Delete specific news article | ✅ (Admin) |

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

# Run all tests (14 test modules)
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test categories
pytest tests/test_api_*.py -v              # All API endpoint tests
pytest tests/test_ai_function.py -v        # AI integration tests
pytest tests/test_audio_synthesis.py -v    # TTS audio processing tests
pytest tests/test_ipa_phonetic.py -v       # IPA phonetic transcription tests
pytest tests/test_connection.py -v         # Database connection tests
pytest tests/test_endpoint_auth.py -v      # Authentication tests
pytest tests/test_login.py -v              # Login functionality tests
pytest tests/test_search_words.py -v       # Search functionality tests
pytest tests/test_WOTD.py -v               # Word of the Day tests

# Run tests with detailed output
pytest -v --tb=short

# Run tests with coverage and HTML report
pytest --cov=app --cov-report=html tests/
```

### Test Structure
- **Unit Tests**: Individual component testing across 14 specialized modules
- **Integration Tests**: API endpoint testing with authentication validation
- **Database Tests**: Connection and transaction testing for PostgreSQL
- **Authentication Tests**: Complete security mechanism verification
- **AI Integration Tests**: External service testing with mock responses
- **Audio Processing Tests**: TTS synthesis and audio file validation
- **IPA Phonetic Tests**: Phonetic transcription accuracy and formatting
- **Search Tests**: Word search and discovery functionality validation
- **User Management Tests**: Registration, role-based access, and permission testing
- **Progress Tracking Tests**: Learning progress accuracy and consistency validation
- **Word Management Tests**: CRUD operations, duplicate detection, and data integrity
- **News API Tests**: Content delivery and filtering functionality
- **Error Handling Tests**: Comprehensive exception management and edge case coverage
- **Performance Tests**: Response time and resource usage validation

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
- **Comprehensive Logging**: Structured logging with file (`app.log`) and console output
- **Database Connection Monitoring**: Real-time connection status and health validation
- **AI Service Monitoring**: Request/response tracking for external services
- **Performance Metrics**: Response time tracking and resource usage monitoring
- **Health Endpoints**: Multiple health check endpoints for deployment monitoring
- **Scheduler Monitoring**: Background task execution tracking and error reporting

### Monitoring Endpoints
- **Health Check**: `GET /health` - Comprehensive application health status
- **Root Status**: `GET /` - Basic application availability
- **Cache Info**: `GET /tts/cache/info` - TTS cache statistics and performance
- **Static Files**: `GET /static/*` - Media file access and delivery monitoring

### Log Files
- **Application Logs**: `app.log` (in project root)
- **Error Tracking**: Comprehensive error logging with stack traces
- **Performance Logs**: Request timing and resource usage
- **Scheduler Logs**: Background task execution and timing information

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
# Error: connection to PostgreSQL failed
# Solution: Check connection string and credentials
```
- **Connection Issues**: Verify PostgreSQL connection string format
- **Credentials**: Ensure database credentials are correct in .env file
- **Network**: Check network connectivity to database host

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
- **Alternative API Docs**: http://localhost:8000/redoc (when running)

### Support Channels
- **Issues**: GitHub Issues for bug reports and feature requests
- **Development**: Check `docs/Progress.md` for current development status
- **Configuration**: Refer to this README for setup and configuration guidance

---

## 📄 License

This project is part of the MSE800 Post School Education program at YooBee Colleges.

---

## 🔄 Changelog

### Version 1.3 (July 12, 2025)
- ✅ **Enhanced Testing Infrastructure**: 14 specialized test modules with comprehensive coverage
- ✅ **Audio Processing Enhancement**: TTS audio synthesis testing with comprehensive validation
- ✅ **IPA Phonetic Integration**: Enhanced phonetic transcription support for accurate pronunciation
- ✅ **Production Deployment Ready**: Render.com deployment configuration with health monitoring
- ✅ **Router-Based Architecture**: Modular endpoint organization with dedicated router modules
- ✅ **Configuration Management**: JSON-based settings with environment-specific configurations

### Version 1.3 (July 12, 2025) - Current
- ✅ **Advanced Testing Framework**: Enhanced test infrastructure with 14 specialized test modules
- ✅ **Quality Assurance Enhancement**: Comprehensive endpoint coverage and role-based testing
- ✅ **Test Automation**: Advanced fixtures and mocking framework for reliable testing
- ✅ **Data Integrity Testing**: Cross-user data isolation and transaction integrity verification
- ✅ **Edge Case Coverage**: Comprehensive testing of invalid inputs and error handling scenarios

### Version 1.1 (July 2, 2025)
- ✅ **Database Migration & Production Scaling**: PostgreSQL integration with Supabase cloud hosting
- ✅ **PostgreSQL-Only Configuration**: Unified PostgreSQL environment for all deployments
- ✅ **Enhanced Performance**: Improved query performance and connection pooling
- ✅ **Testing Infrastructure**: Comprehensive test suite with database isolation
- ✅ **Production Readiness**: Cloud database architecture for high-availability deployment

### Previous Versions
- **v0.9**: Core API functionality with basic authentication
- **v0.8**: AI integration with Google Gemini and AWS Polly
- **v0.7**: Database models and CRUD operations
- **v0.6**: Initial FastAPI setup and project structure

---

*Last Updated: July 12, 2025*  
*Status: Production Ready with Enhanced Documentation & Testing Infrastructure*
