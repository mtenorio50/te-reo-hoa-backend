# Te Reo Hoa

Te Reo Hoa is a learning web application that helps users engage with and learn Te Reo Māori. It offers features like vocabulary translation, AI-generated learning content, and audio pronunciation. Designed for students and educators, it includes role-based access (admin/learner), JWT authentication, and future support for progress tracking.

---

## Features

- JWT Authentication
- Role-based user management (admin, staff, learner)
- Vocabulary and phrase content management
- AI-powered translation and example generation (Gemini API)
- Māori Text-to-Speech audio (Azure or Gemini voice)
- CORS-ready API for frontend integration
- Plans for user progress tracking and gamification

---

## Tech Stack

| Layer        | Tech                     |
|--------------|--------------------------|
| Backend      | FastAPI (Python)         |
| AI           | Google Gemini API        |
| Database     | SQLite                   |
| Deployment   | Render                   |
| Frontend     | Typescript               |

---

## 🔧 Setup

1. Clone the repo  
2. Create `.env` file with your keys:
