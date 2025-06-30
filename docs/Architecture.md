# Te Reo Hoa - System Architecture

## 🏗️ Overview

Te Reo Hoa is a comprehensive language learning platform focused on English-to-Māori translation, vocabulary management, user progress tracking, and AI-powered content delivery. The architecture follows a modern, modular design with clear separation of concerns, scalable components, and robust error handling.

**Current Version**: v1.0 - Production Ready Backend  
**Last Updated**: June 30, 2025

---

## 🎯 System Design Principles

- **Modularity**: Clean separation with router-based API organization
- **Scalability**: Database-agnostic design with SQLAlchemy ORM
- **Security**: JWT-based authentication with role-based access control  
- **Reliability**: Comprehensive error handling and data validation
- **Extensibility**: Plugin-ready AI integrations and service abstractions
- **Cross-Platform**: Consistent behavior across Windows, macOS, and Linux
- **Developer Experience**: Intelligent configuration with automatic setup

---

## 🚀 **Recent Architecture Enhancements (June 30, 2025)**

### **Infrastructure Improvements**
- **Enhanced Database Layer**: Robust SQLite configuration with automatic directory creation
- **Intelligent Path Resolution**: Advanced cross-platform path handling system
- **Error Recovery Mechanisms**: Comprehensive database connection error handling
- **Environment Configuration**: Streamlined setup with intelligent fallback systems
- **Login Endpoint Optimization**: Dual-path support resolving 307 redirect issues

### **Configuration Management Evolution**
- **Auto-provisioning**: Automatic creation of database directories and files
- **Flexible Setup**: Support for both development and production configurations
- **Debug Integration**: Real-time database path and connection status reporting
- **Cross-Platform Compatibility**: Consistent behavior across different operating systems
- **Graceful Degradation**: Robust fallback mechanisms for missing configurations

---

## 🏛️ Architecture Layers

### 1. **Presentation Layer (API)**
**Technology**: FastAPI with automatic OpenAPI documentation

**Endpoints**:
- `/login` - Authentication and token management (dual-path support)
- `/users` - User management and role administration  
- `/words` - Vocabulary CRUD operations with AI integration
- `/translate` - Direct translation services
- `/progress` - User learning progress tracking
- `/quiz` - Interactive learning assessments
- `/news` - Curated positive news content

**Features**:
- Automatic request/response validation with Pydantic schemas
- Interactive API documentation (Swagger/ReDoc)
- CORS middleware for frontend integration
- Comprehensive error handling with HTTP status codes
- Dual-path endpoint support for better compatibility

### 2. **Business Logic Layer**

**Authentication & Authorization** (`auth.py`):
- JWT token generation and validation
- Role-based access control (admin, learner)
- Password hashing with secure algorithms
- Token expiration and refresh logic

**CRUD Operations** (`crud.py`):
- Database abstraction layer
- Optimized queries with SQLAlchemy
- Data validation and sanitization
- Relationship management

**AI Integration** (`ai_integration.py`):
- Google Gemini API for translation and content generation
- AWS Polly for Māori text-to-speech synthesis
- Extended timeout handling (120 seconds)
- Response parsing and error handling
- Configurable AI model parameters

**Utilities** (`utils.py`):
- Input sanitization and normalization
- JSON parsing from AI responses
- Text processing utilities
- Level and domain validation

### 3. **Data Layer**

**Database Configuration** (`database.py`):
- Intelligent SQLite setup with automatic directory creation
- Cross-platform path resolution
- Environment variable handling with fallbacks
- Real-time connection status monitoring
- Debug logging for troubleshooting

**Database Models** (`models.py`):
```python
User:
- id, email, hashed_password, role, created_at

Word:
- id, text, translation, level, type, domain
- example, audio_url, normalized, notes

UserWordProgress:
- user_id, word_id, status, updated_at
- status: unlearned, learned, review, starred

NewsItem:
- id, title_english, title_maori
- summary_english, summary_maori
- published_date, source_url, source
- image_urls (JSON), created_at
```

**Schemas** (`schemas.py`):
- Pydantic models for request/response validation
- Type safety and automatic documentation
- Input sanitization and output formatting

---

## 🔄 Data Flow Architecture

```
[ Frontend Client ]
        ↓ HTTP Requests
[ CORS Middleware ]
        ↓
[ FastAPI Router ]
        ↓
[ Authentication Layer ]
        ↓
[ Business Logic ]
    ↙     ↓     ↘
[Database] [AI Services] [Audio Generation]
    ↓
[ Auto-Provisioned Storage ]
```

### Enhanced Request Flow Example (Add Word):

1. **Client Request**: POST `/words/add` with word data
2. **Authentication**: Verify JWT token and admin role
3. **Validation**: Pydantic schema validation
4. **Database Check**: Auto-create directories if needed
5. **Duplicate Check**: Query database for existing word
6. **AI Translation**: Call Gemini API for translation
7. **Data Processing**: Parse and sanitize AI response
8. **Database Insert**: Create word record with error handling
9. **Audio Generation**: Generate pronunciation with AWS Polly
10. **Response**: Return complete word object

---

## 🗄️ Database Design

### Enhanced Database Architecture

**File Structure**:
```
te-reo-hoa-backend/
├── data/                    # Auto-created database directory
│   └── te_reo_hoa.db       # SQLite database file
├── app/
│   └── database.py         # Enhanced configuration
└── .env                    # Environment configuration
```

### Entity Relationship Diagram

```
Users (1) ←→ (N) UserWordProgress (N) ←→ (1) Words
                     ↓
               Progress Tracking
                     ↓
            NewsItem (Independent)
```

### Advanced Database Features

**Auto-Provisioning System**:
- Automatic creation of `/data` directory if missing
- Intelligent path resolution for cross-platform compatibility
- Real-time database status monitoring
- Graceful fallback for missing configurations

**Enhanced Schema**:
- **Users Table**: Authentication and role management with extensible roles
- **Words Table**: Comprehensive vocabulary with normalized search support
- **UserWordProgress Table**: Learning status tracking with timestamps
- **NewsItem Table**: Bilingual news content with JSON metadata support

**Optimization Features**:
```sql
-- Strategic indexing for performance
CREATE INDEX idx_words_normalized ON words(normalized);
CREATE INDEX idx_words_level ON words(level);
CREATE INDEX idx_progress_user_status ON user_word_progress(user_id, status);
CREATE INDEX idx_news_source_url ON news(source_url);
```

---

## 🤖 AI Integration Architecture

### Google Gemini Integration

**Enhanced Translation Service**:
- Prompt engineering for consistent bilingual output
- Extended timeout handling (120 seconds)
- JSON response parsing with fallback mechanisms
- Rate limiting and error retry logic
- Response validation and sanitization

**News Content Processing**:
- Real-time RSS feed processing
- AI-powered positivity analysis and filtering
- Bilingual content summarization
- Image extraction and URL validation
- Source tracking and duplicate prevention

### AWS Polly Integration

**Advanced Text-to-Speech Pipeline**:
- Māori text normalization and processing
- Voice selection and parameter optimization
- Audio file generation with unique naming
- Static file serving integration
- URL generation for frontend access

---

## 🔒 Enhanced Security Architecture

### Authentication Flow

```
1. User Login → Credential Validation → JWT Generation
2. API Request → Token Extraction → Validation & Decode
3. Authorization → Role Check → Allow/Deny Access
4. Dual-Path Support → Handle Both /endpoint and /endpoint/
```

### Security Measures

- **Password Security**: Bcrypt hashing with salt
- **Token Security**: JWT with configurable expiration
- **API Security**: Role-based endpoint protection with dual-path support
- **Input Validation**: Comprehensive Pydantic schema enforcement
- **SQL Injection Prevention**: SQLAlchemy ORM parameterization
- **CORS Configuration**: Controlled origin access for frontend integration
- **Environment Security**: Secure configuration with fallback mechanisms

---

## 📁 Enhanced File Organization

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
├── 📊 data/                   # Auto-created database storage
│   └── te_reo_hoa.db         # SQLite database file
├── 🔊 static/                 # Static file serving
│   └── audio/                # Generated pronunciation files
│       └── tts_cache/        # Cached TTS audio files
├── ⚙️ config/                # Configuration files
│   └── settings.json         # Admin and application settings
├── 📚 docs/                   # Project documentation
│   ├── Architecture.md       # System architecture guide
│   └── Progress.md           # Development timeline
├── 🧪 tests/                  # Test suite
│   └── test_basic.py         # Basic functionality tests
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # README file
```

---

## 🚀 Deployment Architecture

### Development Environment
```
Developer Machine
├── Python Virtual Environment
├── Auto-Created SQLite Database (/data directory)
├── Local FastAPI Server (Uvicorn with auto-reload)
├── Environment Variables (.env file)
└── Direct API Key Access
```

### Enhanced Production Environment
```
Production Server
├── Gunicorn WSGI Server
│   └── Multiple Uvicorn Workers
├── PostgreSQL Database (production upgrade)
│   └── Connection Pooling
├── Reverse Proxy (Nginx)
│   ├── SSL Termination
│   ├── Static File Serving
│   └── Load Balancing
├── Auto-Created Directory Structure
└── Environment Variable Management
```

### Scaling Considerations

**Horizontal Scaling**:
- Stateless API design enables multiple instances
- Auto-provisioning works across multiple servers
- Database connection pooling for concurrent requests
- External service rate limiting and caching

**Performance Optimization**:
- Intelligent database path resolution
- AI response caching for repeated translations
- Audio file CDN distribution
- Background task processing for non-critical operations

---

## 🔍 Monitoring & Observability

### Enhanced Logging Strategy
- **Real-time Database Status**: Connection monitoring and path validation
- **Configuration Debugging**: Environment variable loading and fallback usage
- **Request/Response Logging**: Performance metrics and error tracking
- **AI Service Interaction**: Detailed logging for external service calls
- **Cross-Platform Monitoring**: OS-specific path and behavior tracking

### Health Checks
- **Database Connectivity**: Auto-provisioning status and connection health
- **External Service Availability**: AI and audio service monitoring
- **File System Permissions**: Directory creation and write access validation
- **Performance Monitoring**: Response time and resource usage tracking

---

## 🔄 Integration Points

### Frontend Integration
- **RESTful API**: Consistent response formats with comprehensive error handling
- **CORS Configuration**: Secure browser integration with multiple origin support
- **Real-time Capabilities**: WebSocket support for future enhancements
- **File Serving**: Static audio file delivery with proper caching headers

### External Services
- **Google Gemini**: Enhanced translation with extended timeout handling
- **AWS Polly**: Audio synthesis with intelligent file management
- **News Sources**: RSS feed integration with duplicate prevention
- **CDN Integration**: Static file distribution for audio content

---

## 🛣️ Future Architecture Enhancements

### Planned Improvements
- **Microservices Migration**: Service decomposition for better scalability
- **Event-Driven Architecture**: Asynchronous processing with message queues
- **Enhanced Caching**: Redis integration for performance optimization
- **API Versioning**: Backward compatibility with version management
- **Container Orchestration**: Kubernetes deployment with auto-scaling
- **Real-time Features**: WebSocket integration for live interactions

### Technology Roadmap
- **Database Evolution**: PostgreSQL migration with advanced features
- **Search Enhancement**: Elasticsearch for full-text search capabilities
- **Analytics Platform**: User behavior tracking and learning insights
- **Mobile API**: GraphQL endpoint for mobile applications
- **AI/ML Pipeline**: Custom model training and deployment infrastructure

---

## 📊 Architecture Quality Metrics

### **Current Architecture Statistics**
- **API Endpoints**: 15 endpoints with dual-path support
- **Database Models**: 4 comprehensive models with auto-provisioning
- **Configuration Management**: Intelligent environment handling with fallbacks
- **Cross-Platform Support**: Windows, macOS, and Linux compatibility
- **Error Recovery**: Enhanced debugging and troubleshooting capabilities
- **Developer Experience**: Streamlined setup with automatic configuration

### **Architecture Principles Achieved**
- ✅ **Modularity**: Clean router-based organization
- ✅ **Scalability**: Database-agnostic with auto-provisioning
- ✅ **Reliability**: Comprehensive error handling and recovery
- ✅ **Security**: Role-based access with dual-path endpoint support
- ✅ **Maintainability**: Clear separation of concerns and documentation
- ✅ **Extensibility**: Plugin-ready AI and service integrations
- ✅ **Cross-Platform**: Consistent behavior across operating systems
- ✅ **Developer-Friendly**: Intelligent configuration and setup automation

---

## 📞 Architecture Support

**System Architecture**: Modular FastAPI with intelligent configuration  
**Database Layer**: Auto-provisioning SQLite with cross-platform support  
**Integration Layer**: Enhanced AI services with extended timeout handling  
**Security Model**: JWT-based authentication with dual-path endpoint support  

---

*Architecture Document Version: 2.0*  
*Last Updated: June 30, 2025*  
*Status: Production Ready with Enhanced Infrastructure*