# Progress Log

## 17 June 2025

### New Features Implemented

- **Word of the Day:**  
  Implemented a daily rotating word endpoint that serves a random word with full details to all registered users.

- **User Progress Tracking:**  
  Added endpoints and data model for users to mark words as "learned", "to review", "starred", and "unlearned".  
  Included a stats endpoint for users to see their progress counts and list their learned words.

- **Quiz/Practice Endpoints:**  
  Added quiz endpoints for multiple-choice vocabulary practice, including answer checking and scoring logic.

- **Search & Filter Words:**  
  Users can now search and filter vocabulary by level, type, domain, and text.

- **Positive News Feed:**  
  Integrated `/news/` endpoint that fetches Māori news from RNZ Te Ao Māori and Te Ao Māori News,  
  then uses Google Gemini AI to filter and return only positive, uplifting stories.  
  Each news item includes title, link, summary, thumbnail, and category.

---

## Recent Fixes & Improvements

- Ensured case-insensitive and strict filtering on word search endpoints.
- Enforced validation and error reporting for non-matching filters.
- Improved AI integration error handling for news filtering.
- Added support for image/thumbnail and category in news stories.
- Re-model routers for a clean main

## 15 June 2025
- Requested a daily progress document and log.
- Continued backend development and testing for Te Reo Hoa endpoints.
- Clarified error handling and validation for word addition (e.g., trimming spaces, lowercase normalization).
- Discussed edge test cases and documentation strategies.
- Planned for CORS setup for frontend-backend integration.
- Started drafting waterfall and agile methodology diagrams for the Car Rental OOP project.
- Requested assistance with Lucidchart and PlantUML for system design documentation.


## 14 June 2025 
- Worked on the **Te Reo Hoa** backend, focusing on user progress tracking endpoints.
- Debugged and addressed issues with marking word progress (learned, review, starred, unlearned, etc.).
- Investigated and fixed error:  
  `AttributeError: 'str' object has no attribute 'get'`
- Reviewed logic for adding new words, especially level validation (basic/intermediate).
- Generated and reviewed a list of 50 basic English-to-Māori words for initial app seeding.
- Planned and prioritized next features (user progress tracking vs. daily word).


