# Te Reo Hoa - System Architecture

## 🏗️ Overview

Te Reo Hoa is a comprehensive language learning platform focused on English-to-Māori translation, vocabulary management, user progress tracking, and AI-powered content delivery. The architecture follows a modern, modular design with clear separation of concerns, scalable components, and robust error handling.

**Current Version**: v1.1 - Enhanced Production Backend with PostgreSQL Migration  
**Last Updated**: July 2, 2025

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

## 🚀 **Recent Architecture Enhancements (July 2, 2025)**

### **Database Migration & Production Scaling**
- **PostgreSQL Integration**: Successfully migrated from SQLite to PostgreSQL for enhanced scalability
- **Cloud Database**: Supabase PostgreSQL integration for production-grade data management
- **Dual Database Support**: Maintained SQLite for development while using PostgreSQL for production
- **Enhanced Performance**: Improved query performance and connection pooling with PostgreSQL
- **Testing Infrastructure**: Comprehensive test suite with 9 specialized test modules

### **Production Readiness Improvements**
- **Cloud Integration**: Seamless Supabase PostgreSQL connection with secure authentication
- **Test Coverage**: Advanced testing framework covering all major functionality areas
- **Database Optimization**: Enhanced connection management and transaction handling
- **Scalability**: Production-ready database architecture for high-availability deployment
- **Configuration Management**: Dual-environment configuration supporting both development and production

---

## 🚀 **Previous Architecture Enhancements (June 30, 2025)**

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
- **PostgreSQL Production Database**: Supabase cloud integration for scalable data management
- **Dual Database Support**: SQLite for development, PostgreSQL for production environments
- **Enhanced Connection Management**: Advanced connection pooling and transaction handling
- **Cloud Database Security**: Secure authentication and encrypted connections
- **Cross-Platform Compatibility**: Consistent behavior across development and production environments

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

**Database Architecture**:
- **Production**: PostgreSQL on Supabase with advanced features and scalability
- **Development**: SQLite with auto-provisioning for local development
- **Testing**: Isolated test database configuration for comprehensive testing
- **Migration**: Seamless migration path from SQLite to PostgreSQL

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

**Database Infrastructure**:
```
te-reo-hoa-backend/
├── Production Environment:        # PostgreSQL on Supabase
│   └── Supabase PostgreSQL        # Cloud-hosted production database
├── Development Environment:       # SQLite with auto-provisioning
│   ├── data/                      # Auto-created database directory
│   └── te_reo_hoa.db             # Local SQLite database file
├── Testing Environment:           # Isolated test database
│   └── test.db                    # Dedicated test database
└── app/
    └── database.py                # Dual-database configuration
```

### Database Configuration Management

**Production Configuration**:
- **Primary Database**: PostgreSQL on Supabase cloud infrastructure
- **Connection String**: `POSTGRE_SQLALCHEMY_DATABASE_URL` environment variable
- **Features**: Advanced PostgreSQL features, connection pooling, cloud backup
- **Scalability**: High-availability setup with automatic scaling

**Development Configuration**:
- **Local Database**: SQLite with auto-provisioning
- **Connection String**: `SQLALCHEMY_DATABASE_URL` for local development
- **Features**: Automatic directory creation, cross-platform compatibility
- **Development Experience**: Zero-configuration setup for new developers

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
- **API Endpoints**: 15 endpoints with comprehensive testing coverage
- **Database Models**: 4 comprehensive models optimized for PostgreSQL
- **Database Backend**: PostgreSQL on Supabase with enhanced performance
- **Test Coverage**: 9 specialized test modules covering all major functionality
- **Configuration Management**: Dual-environment database support (PostgreSQL/SQLite)
- **Cloud Integration**: Supabase PostgreSQL with secure cloud-based data management
- **Authentication System**: Advanced JWT implementation with comprehensive test validation

### **Architecture Principles Achieved**
- ✅ **Modularity**: Clean router-based organization with comprehensive testing
- ✅ **Scalability**: PostgreSQL migration for production-grade performance
- ✅ **Reliability**: Comprehensive error handling and recovery with test validation
- ✅ **Security**: Role-based access with complete authentication testing
- ✅ **Maintainability**: Clear separation of concerns and comprehensive documentation
- ✅ **Extensibility**: Plugin-ready AI and service integrations with test coverage
- ✅ **Production Ready**: Cloud database integration with Supabase PostgreSQL
- ✅ **Test Coverage**: 9 specialized test modules ensuring system reliability

---

## 📞 Architecture Support

**System Architecture**: Modular FastAPI with PostgreSQL cloud database integration  
**Database Layer**: Production PostgreSQL on Supabase with development SQLite support  
**Integration Layer**: Enhanced AI services with comprehensive test coverage  
**Security Model**: JWT-based authentication with complete testing validation  

---

*Architecture Document Version: 2.1*  
*Last Updated: July 2, 2025*  
*Status: Production Ready with PostgreSQL Migration and Enhanced Testing*