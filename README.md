🧠 Overview
The AI Study Assistant is a Flask-based web application that transforms uploaded PDF notes into interactive learning materials using Google Gemini AI. It generates quizzes and flashcards, evaluates user answers, and tracks performance over time using a database.
The system is designed to simulate a smart revision tool similar to EdTech platforms like Quizlet or Duolingo, with AI-powered grading and feedback.
________________________________________
🎯 Key Features
1. 📄 PDF Upload & Text Extraction
•	Users upload a PDF file
•	The system extracts raw text using PyPDF
•	Extracted content is used as input for AI generation
Tech used:
•	PyPDF (PdfReader)
•	Flask file handling
________________________________________
2. 🤖 AI Quiz Generation (Gemini API)
The app uses Google Gemini (gemini-2.5-flash) to:
•	Generate 10 quiz questions
•	Generate 10 flashcards
•	Ensure structured output using prompt engineering
Prompt strategy:
•	Strict formatting rules
•	No explanation or extra text
•	Output structured as JSON or numbered questions
________________________________________
3. 🧠 Flashcard System
•	Flashcards are generated in JSON format:
[
  {"q": "Question", "a": "Answer"}
]
UI behavior:
•	Front shows question
•	Back reveals answer on click (flip interaction)
________________________________________
4. 📝 Quiz System
•	Users answer AI-generated questions
•	Each question is displayed dynamically in HTML
•	Hidden fields store:
o	correct answer
o	question text
________________________________________
5. 📊 Quiz Scoring System (Initial Version)
Originally implemented using:
if user_answer.lower() == correct_answer.lower():
    score += 1
Then improved to:
•	Flexible string matching
•	Partial correctness handling
________________________________________
6. 🤖 AI Grading System (Gemini Upgrade)
Upgraded system uses Gemini as an examiner model.
Workflow:
1.	Collect all questions + answers
2.	Send to Gemini in a single request
3.	Gemini returns structured grading:
[
  {
    "correct": true,
    "feedback": "Good understanding of concept"
  }
]
Benefits:
•	Accepts paraphrasing
•	Handles scientific equivalence
•	Provides feedback per question
•	Mimics human marking
________________________________________
7. 📈 Score Calculation & Feedback
The system:
•	Computes final score
•	Displays per-question breakdown
•	Shows:
o	user answer
o	correct answer
o	AI feedback
o	correctness indicator
________________________________________
8. 🗄️ Database Integration (SQLite)
Database: study.db
Stores quiz history:
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER,
    total INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
Features:
•	Stores quiz attempts
•	Tracks performance over time
•	Enables history page
________________________________________
9. 📊 Progress History Page
•	Displays past quiz attempts
•	Shows score + timestamp
•	Acts as simple analytics system
________________________________________
10. ⬇️ Export Features
Users can download results as:
TXT
•	Plain text version of quiz results
PDF
•	Generated using ReportLab
•	Converts quiz output into downloadable document
________________________________________
11. ⚠️ Error Handling & Reliability Improvements
Issues handled:
•	Gemini busy / API failure (retry logic)
•	JSON parsing errors from AI output
•	PDF extraction failures
Improvements:
•	Retry loop for API calls
•	Regex cleanup of AI output
•	Fallback error messages
________________________________________
12. 🧱 Architecture Overview
PDF Upload
   ↓
Text Extraction (PyPDF)
   ↓
Gemini Prompt (Quiz/Flashcards)
   ↓
Frontend Display (Flask + HTML)
   ↓
User Answers Input
   ↓
Gemini Grading (AI evaluation)
   ↓
Score + Feedback Display
   ↓
SQLite Storage (History)
________________________________________
🧰 Tech Stack
Backend:
•	Python
•	Flask
•	SQLite
AI:
•	Google Gemini API
PDF Processing:
•	PyPDF
Export:
•	ReportLab
Frontend:
•	HTML
•	Jinja2 templates
•	Basic CSS (custom styling)
________________________________________
🚀 Key Design Decisions
1. AI vs Traditional Grading
•	Initially used string matching
•	Upgraded to AI-based evaluation for semantic understanding
________________________________________
2. Single API call grading
•	All answers sent in one request
•	Reduces cost and latency
________________________________________
3. Hidden fields in HTML
•	Used to pass correct answers securely to backend
________________________________________
4. SQLite over cloud DB
•	Lightweight
•	Easy local development
•	Perfect for early-stage portfolio
________________________________________
⚠️ Known Limitations
•	Gemini output occasionally requires JSON cleanup
•	No user authentication yet
•	No real-time concurrency handling
•	Basic UI (no frontend framework)
•	No persistent cloud deployment yet
________________________________________
🔮 Future Improvements
Short-term
•	Dashboard with analytics
•	Wrong answer review system
•	Better UI styling
Medium-term
•	User accounts (login system)
•	Topic-based quizzes
•	Progress tracking charts
Advanced
•	Adaptive learning system
•	Personalized revision plans
•	Multi-document knowledge base
________________________________________


