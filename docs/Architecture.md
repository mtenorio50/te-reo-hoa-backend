# Te Reo Hoa - System Architecture

## 🏗️ Overview

Te Reo Hoa is a comprehensive language learning platform focused on English-to-Māori translation, vocabulary management, user progress tracking, and AI-powered content delivery. The architecture follows a modern, modular design with clear separation of concerns, scalable components, and robust error handling.

**Current Version**: v1.3 - Enhanced Documentation & Testing Infrastructure  
**Last Updated**: July 12, 2025

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

## 🚀 **Latest Architecture Enhancements (July 12, 2025)**

### **Enhanced Documentation & Testing Infrastructure**
- **Comprehensive Test Coverage**: Expanded to 14 specialized test modules covering all critical functionality
- **Audio Processing Enhancement**: Added TTS audio synthesis testing with comprehensive audio validation
- **IPA Phonetic Integration**: Enhanced phonetic transcription support for accurate pronunciation testing
- **Production Deployment Ready**: Render.com deployment configuration with health monitoring endpoints
- **Router-Based Architecture**: Modular endpoint organization with dedicated router modules

### **Database Architecture Modernization**
- **PostgreSQL-Only Configuration**: Streamlined to use only PostgreSQL for both development and production
- **Supabase Cloud Integration**: Enhanced cloud database configuration with secure connection management
- **Simplified Configuration**: Removed dual-database complexity, focusing on production-grade PostgreSQL
- **Enhanced Connection Management**: Improved database session handling and connection pooling
- **Configuration Management**: JSON-based settings with environment-specific configurations

---

## 🚀 **Previous Architecture Enhancements (July 10, 2025)**

### **Advanced Testing Framework & Quality Assurance**
- **Comprehensive Test Coverage**: Expanded testing infrastructure with advanced fixtures and mocking
- **Quality Assurance Enhancement**: Complete endpoint coverage with authentication and authorization testing
- **Role-Based Testing**: Comprehensive testing of admin vs learner permissions and data isolation
- **Test Automation**: Advanced mocking and fixture management with AI integration testing
- **Edge Case Coverage**: Complete testing of invalid inputs, unauthorized access, and error handling scenarios

---

## 🚀 **Previous Architecture Enhancements (July 2, 2025)**

### **Database Migration & Production Scaling**
- **PostgreSQL Integration**: Successfully migrated from SQLite to PostgreSQL for enhanced scalability
- **Cloud Database**: Supabase PostgreSQL integration for production-grade data management
- **Enhanced Performance**: Improved query performance and connection pooling with PostgreSQL
- **Testing Infrastructure**: Comprehensive test suite development
- **Configuration Management**: Environment-based configuration supporting production deployment

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
- `/tts` - Text to speech service

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
- **PostgreSQL-Only Architecture**: Streamlined configuration using only PostgreSQL
- **Supabase Cloud Integration**: Production-grade cloud database hosting
- **Enhanced Connection Management**: Advanced connection pooling and session handling
- **Environment-Based Configuration**: Uses `POSTGRE_SQLALCHEMY_DATABASE_URL` environment variable
- **Secure Authentication**: Encrypted connections with secure credential management

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
├── Development Environment:       # PostgreSQL configuration
│   └── PostgreSQL via Supabase    # Unified PostgreSQL environment
├── Testing Environment:           # PostgreSQL test configuration
│   └── Test Database              # Dedicated test database setup
└── app/
    └── database.py                # PostgreSQL-only configuration
```

### Database Configuration Management

**PostgreSQL Configuration**:
- **Primary Database**: PostgreSQL on Supabase cloud infrastructure
- **Connection String**: `POSTGRE_SQLALCHEMY_DATABASE_URL` environment variable
- **Features**: Advanced PostgreSQL features, connection pooling, cloud backup
- **Scalability**: High-availability setup with automatic scaling
- **Environment Unified**: Single PostgreSQL configuration for all environments

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
│   │   ├── admin.py          # Admin management endpoints
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── news.py           # News content management
│   │   ├── phrase.py         # Te Reo phrase management
│   │   ├── pronunciation.py  # Audio pronunciation features
│   │   ├── quiz.py           # Interactive quiz system
│   │   ├── system.py         # System health and monitoring
│   │   ├── translation.py    # AI-powered translation services
│   │   └── user.py           # User profile management
│   ├── __init__.py           # Application package initialization
│   ├── ai_integration.py     # Google Gemini AI integration
│   ├── auth.py               # JWT authentication and authorization
│   ├── crud.py               # Database CRUD operations
│   ├── database.py           # PostgreSQL database configuration
│   ├── db_initialize.py      # Database initialization and setup
│   ├── main.py               # FastAPI application entry point
│   ├── models.py             # SQLAlchemy database models
│   ├── schemas.py            # Pydantic response/request schemas
│   └── utils.py              # Utility functions and helpers
├── 📚 docs/                  # Project documentation
│   ├── Architecture.md       # System architecture guide
│   └── Progress.md           # Development timeline
├── 🧪 tests/                 # Comprehensive test suite (14 modules)
│   ├── conftest.py           # Test configuration and fixtures
│   ├── test_basic.py         # Basic functionality tests
│   ├── test_admin.py         # Admin endpoint tests
│   ├── test_ai_integration.py # AI integration tests
│   ├── test_auth.py          # Authentication tests
│   ├── test_crud.py          # Database CRUD tests
│   ├── test_database.py      # Database configuration tests
│   ├── test_db_initialize.py # Database initialization tests
│   ├── test_main.py          # Main application tests
│   ├── test_models.py        # Database model tests
│   ├── test_news.py          # News system tests
│   ├── test_phrase.py        # Phrase management tests
│   ├── test_pronunciation.py # Pronunciation feature tests
│   ├── test_schemas.py       # Schema validation tests
│   └── test_utils.py         # Utility function tests
├── README.md                 # Project documentation and setup guide
├── requirements.txt          # Python dependencies
├── main.py                   # Application entry point
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
- **API Endpoints**: 14 endpoints with comprehensive testing coverage
- **Database Models**: 4 comprehensive models optimized for PostgreSQL
- **Database Backend**: PostgreSQL-only configuration on Supabase cloud platform
- **Test Coverage**: 14 specialized test modules covering all major functionality
- **Configuration Management**: Unified PostgreSQL environment for all deployments
- **Cloud Integration**: Supabase PostgreSQL with secure cloud-based data management
- **Authentication System**: Advanced JWT implementation with comprehensive test validation
- **Quality Assurance**: Complete API testing with role-based access and data integrity verification

### **Architecture Principles Achieved**
- ✅ **Modularity**: Clean router-based organization with comprehensive testing
- ✅ **Scalability**: PostgreSQL migration for production-grade performance
- ✅ **Reliability**: Comprehensive error handling and recovery with test validation
- ✅ **Security**: Role-based access with complete authentication testing
- ✅ **Maintainability**: Clear separation of concerns and comprehensive documentation
- ✅ **Extensibility**: Plugin-ready AI and service integrations with test coverage
- ✅ **Production Ready**: Cloud database integration with Supabase PostgreSQL
- ✅ **Test Coverage**: 14 specialized test modules ensuring system reliability

---

## 📞 Architecture Support

**System Architecture**: Modular FastAPI with PostgreSQL cloud database integration  
**Database Layer**: Production PostgreSQL on Supabase with unified configuration  
**Integration Layer**: Enhanced AI services with comprehensive test coverage  
**Security Model**: JWT-based authentication with complete testing validation  

---

*Architecture Document Version: 1.3*  
*Last Updated: July 12, 2025*  
*Status: Production Ready with Enhanced Documentation & Testing Infrastructure*