# Te Reo Hoa - System Architecture

## 🏗️ Overview

Te Reo Hoa is a comprehensive language learning platform focused on English-to-Māori translation, vocabulary management, user progress tracking, and AI-powered content delivery. The architecture follows a modern, modular design with clear separation of concerns, scalable components, and robust error handling.

---

## 🎯 System Design Principles

- **Modularity**: Clean separation with router-based API organization
- **Scalability**: Database-agnostic design with SQLAlchemy ORM
- **Security**: JWT-based authentication with role-based access control  
- **Reliability**: Comprehensive error handling and data validation
- **Extensibility**: Plugin-ready AI integrations and service abstractions

---

## 🏛️ Architecture Layers

### 1. **Presentation Layer (API)**
**Technology**: FastAPI with automatic OpenAPI documentation

**Components**:
- `/login` - Authentication and token management
- `/users` - User management and role administration  
- `/words` - Vocabulary CRUD operations with AI integration
- `/translate` - Direct translation services
- `/progress` - User learning progress tracking
- `/quiz` - Interactive learning assessments
- `/news` - Curated positive news content

**Features**:
- Automatic request/response validation
- Interactive API documentation (Swagger/ReDoc)
- CORS middleware for frontend integration
- Comprehensive error handling with HTTP status codes

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
- Response parsing and error handling
- Configurable AI model parameters

**Utilities** (`utils.py`):
- Input sanitization and normalization
- JSON parsing from AI responses
- Text processing utilities
- Level and domain validation

**NewsItem Model**:
```python
- id, title_english, title_maori
- summary_english, summary_maori  
- published_date, source_url, source
- image_urls (JSON), created_at
- Unique constraint on source_url

### 3. **Data Layer**

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
```

### Request Flow Example (Add Word):

1. **Client Request**: POST `/words/add` with word data
2. **Authentication**: Verify JWT token and admin role
3. **Validation**: Pydantic schema validation
4. **Duplicate Check**: Query database for existing word
5. **AI Translation**: Call Gemini API for translation
6. **Data Processing**: Parse and sanitize AI response
7. **Database Insert**: Create word record with error handling
8. **Audio Generation**: Generate pronunciation with AWS Polly
9. **Response**: Return complete word object

---

## 🗄️ Database Design

### Entity Relationship Diagram

```
Users (1) ←→ (N) UserWordProgress (N) ←→ (1) Words
```

### Database Schema

**Users Table**:
- Primary authentication and role management
- Supports extensible role system
- Tracks user creation and activity

**Words Table**:
- Comprehensive vocabulary storage
- Normalized text for efficient searching
- Rich metadata (level, type, domain, examples)
- Audio URL for pronunciation files

**UserWordProgress Table**:
- Many-to-many relationship between users and words
- Tracks learning status with enum values
- Timestamped for progress analytics
- Supports spaced repetition algorithms

### Indexing Strategy

```sql
-- Optimized for common query patterns
CREATE INDEX idx_words_normalized ON words(normalized);
CREATE INDEX idx_words_level ON words(level);
CREATE INDEX idx_words_type ON words(type);
CREATE INDEX idx_progress_user_status ON user_word_progress(user_id, status);
```

---

## 🤖 AI Integration Architecture

### Google Gemini Integration

**Translation Service**:
- Prompt engineering for consistent output format
- JSON response parsing with fallback handling
- Rate limiting and error retry logic
- Response validation and sanitization

**News Content Filtering**:
- Real-time RSS feed processing
- AI-powered positivity analysis
- Content summarization and categorization
- Image extraction and URL validation

### AWS Polly Integration

**Text-to-Speech Pipeline**:
- Māori text normalization
- Voice selection and parameter optimization
- Audio file generation and storage
- URL generation for frontend access

---

## 🔒 Security Architecture

### Authentication Flow

```
1. User Login → Verify Credentials → Generate JWT
2. API Request → Extract Token → Validate & Decode
3. Authorization → Check Role → Allow/Deny Access
```

### Security Measures

- **Password Security**: Bcrypt hashing with salt
- **Token Security**: JWT with configurable expiration
- **API Security**: Role-based endpoint protection
- **Input Validation**: Pydantic schema enforcement
- **SQL Injection Prevention**: SQLAlchemy ORM parameterization
- **CORS Configuration**: Controlled origin access

---

## 📁 File Organization

```
app/
├── router/              # API endpoint organization
│   ├── __init__.py     # Router registry
│   ├── users.py        # User management endpoints
│   ├── words.py        # Vocabulary management
│   ├── progress.py     # Learning progress tracking
│   ├── quiz.py         # Assessment functionality
│   ├── translate.py    # Translation services
│   ├── login.py        # Authentication endpoints
│   └── news.py         # News content delivery
├── models.py           # SQLAlchemy database models
├── schemas.py          # Pydantic validation schemas
├── database.py         # Database configuration & connection
├── crud.py             # Database operation abstractions
├── auth.py             # Authentication & authorization logic
├── ai_integration.py   # External AI service integrations
└── utils.py            # Shared utility functions
```

---

## 🚀 Deployment Architecture

### Development Environment
```
Developer Machine
├── Python Virtual Environment
├── SQLite Database
├── Local FastAPI Server (Uvicorn)
└── Direct API Key Access
```

### Production Environment
```
Production Server
├── Gunicorn WSGI Server
│   └── Multiple Uvicorn Workers
├── PostgreSQL Database
│   └── Connection Pooling
├── Reverse Proxy (Nginx)
│   ├── SSL Termination
│   ├── Static File Serving
│   └── Load Balancing
└── Environment Variable Management
```

### Scaling Considerations

**Horizontal Scaling**:
- Stateless API design enables multiple instances
- Database connection pooling for concurrent requests
- External service rate limiting and caching

**Performance Optimization**:
- Database query optimization with proper indexing
- AI response caching for repeated translations
- Audio file CDN distribution
- Background task processing for non-critical operations

---

## 🔍 Monitoring & Observability

### Logging Strategy
- Structured JSON logging for production
- Request/response logging with performance metrics
- Error tracking with stack traces
- AI service interaction logging

### Health Checks
- Database connectivity monitoring
- External service availability checks
- Performance metric collection
- Automated alerting for service degradation

---

## 🔄 Integration Points

### Frontend Integration
- RESTful API with consistent response formats
- Comprehensive error handling with meaningful messages
- CORS configuration for browser security
- Real-time capabilities via WebSocket (future enhancement)

### External Services
- **Google Gemini**: Translation and content analysis
- **AWS Polly**: Audio synthesis and pronunciation
- **News Sources**: RSS feed integration with fallback sources
- **CDN**: Static file distribution for audio content

---

## 🛣️ Future Architecture Enhancements

### Planned Improvements
- **Microservices Migration**: Service decomposition for better scalability
- **Event-Driven Architecture**: Asynchronous processing with message queues
- **Caching Layer**: Redis integration for performance optimization
- **API Versioning**: Backward compatibility with version management
- **Container Orchestration**: Kubernetes deployment with auto-scaling
- **Real-time Features**: WebSocket integration for live interactions

### Technology Roadmap
- **Database Migration**: PostgreSQL with advanced features
- **Search Enhancement**: Elasticsearch for full-text search
- **Analytics Platform**: User behavior tracking and insights
- **Mobile API**: GraphQL endpoint for mobile applications
- **AI/ML Pipeline**: Custom model training and deployment


