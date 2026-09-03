# 📚 AI Study Assistant

An AI-powered learning platform built with **Python and Flask** that converts PDF study notes into quizzes and flashcards using Google Gemini, grades student answers, and tracks learning progress through SQLite.

## 🌐 Live Demo

**Live Application:** https://aistudyassistant-dezn.onrender.com

The deployed application demonstrates the complete workflow, including PDF upload, AI quiz and flashcard generation, answer grading, authentication, dashboard analytics and result exports.

---

# 🚀 Features

### 📄 PDF Upload & Processing

* Upload study notes in PDF format
* Extract text automatically using PyPDF
* Validate PDF file type
* Validate extracted content
* Handle invalid, empty and unsupported PDF inputs

### 🧠 AI Quiz Generation

* Generate **10-question quizzes** from uploaded notes
* Uses Google Gemini for question generation
* Structured JSON output validation
* Automatic retry handling for failed AI responses

### 🎴 AI Flashcards

* Generate **10 flashcards** from uploaded notes
* Interactive flip-card interface
* Responsive presentation for revision

### 🤖 AI-Powered Grading

* Grades student answers semantically using Google Gemini
* Accepts paraphrased answers and equivalent explanations
* Allows minor spelling differences
* Provides feedback for individual answers

### 📊 Dashboard & Analytics

* Total quizzes completed
* Average score
* Best score
* Latest score
* Topic-level performance tracking
* Identifies strong and weak topics

### 📜 Quiz History

* Stores previous quiz attempts using SQLite
* Tracks scores and topic performance
* Displays previous learning activity for each user

### 🔐 User Authentication

* User registration and login
* Password hashing using Werkzeug
* Session-based authentication
* User-specific quiz history and results
* Logout functionality

### ⬇️ Export Options

* Export quiz results as TXT
* Export quiz results as PDF using ReportLab

---

# 🏗️ System Architecture

```text
PDF Upload
     ↓
PDF Validation
     ↓
Text Extraction (PyPDF)
     ↓
Gemini AI Generation
     ↓
Quiz / Flashcards
     ↓
Student Answers
     ↓
Gemini AI Grading
     ↓
Score + Feedback
     ↓
SQLite Database
     ↓
Dashboard & Quiz History
```

---

# 🛠️ Tech Stack

### Backend

* Python
* Flask
* SQLite

### AI

* Google Gemini API
* `google-genai`

### PDF Processing

* PyPDF

### PDF Export

* ReportLab

### Frontend

* HTML
* CSS
* Jinja2 Templates

### Authentication

* Werkzeug password hashing
* Flask sessions

### Deployment

* Render
* Gunicorn
* Production environment variables

---

# 🧩 Reliability & Error Handling

AI-generated content is not guaranteed to return perfectly structured output. The application validates generated responses before displaying them.

The generation pipeline includes:

* Structured JSON validation
* Markdown/code-fence cleanup
* AI response validation
* Up to **3 generation attempts**
* Error handling for failed AI requests
* PDF file validation
* Empty-document detection
* Invalid file handling

---

# 🧠 Semantic Answer Evaluation

Instead of relying solely on exact string matching, the application uses Gemini to evaluate student answers.

This allows the grading system to recognise:

* Paraphrased answers
* Equivalent explanations
* Minor spelling mistakes
* Different wording with the same meaning

The resulting score and topic performance are then stored for later analysis.

---

# 📊 Learning Analytics

Quiz results are stored in SQLite and used to calculate learning statistics.

The dashboard provides:

* Average score
* Best score
* Latest score
* Total quizzes completed
* Topic-level accuracy
* Strong topics
* Weak topics

This allows students to identify areas that may require additional revision.

---

# 🔒 Security

The application includes user-specific data handling and authentication.

Security features include:

* Password hashing using Werkzeug
* Session-based login management
* User-specific quiz history
* Protected application functionality
* Environment variables for sensitive configuration
* `.env` excluded from version control

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/T0493421rayo/AiStudyAssistant.git
cd AiStudyAssistant
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

**Do not commit the `.env` file to GitHub.**

## 5. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 📁 Project Structure

```text
AiStudyAssistant/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── results.html
│   ├── score.html
│   ├── history.html
│   └── dashboard.html
│
├── static/
│   └── style.css
│
└── study.db
```

The database is generated locally by the application and is excluded from version control.

---

# 📈 Benchmark Results

The application was tested using **5 PDF documents** for each generation type.

| Function             | Successful Generations | Average Response Time |
| -------------------- | ---------------------: | --------------------: |
| Quiz generation      |             5/5 (100%) |          28.6 seconds |
| Flashcard generation |             5/5 (100%) |          32.8 seconds |

Each successful generation produced the expected **10 questions or 10 flashcards**.

## Invalid Input Testing

The application was also tested against **3 invalid-input scenarios**:

* Missing PDF
* Non-PDF file
* Empty PDF

These validation scenarios were handled successfully.

> Corrupted-PDF handling is not included in the benchmark figures because it has not yet been independently verified.

---

# 🎯 Future Improvements

Potential future improvements include:

* Automated test suite
* Practice mode for previously incorrect questions
* Score trend visualisations
* More advanced adaptive learning recommendations
* Improved AI response caching
* Expanded analytics and progress tracking
* Additional PDF processing capabilities

---

# 💡 Motivation

Students often spend significant time manually converting lecture notes into revision materials.

This project explores how generative AI can automate that process while providing personalised feedback and progress tracking.

The application combines **AI integration, backend development, database management, document processing and user authentication** into a single full-stack learning platform.

---

# 💻 Key Skills Demonstrated

* Python
* Flask
* Google Gemini API
* Prompt engineering
* AI-assisted semantic evaluation
* SQLite
* Database design
* User authentication
* Password hashing
* Session management
* PDF processing
* JSON validation
* Error handling
* Retry mechanisms
* HTML/CSS
* Jinja2
* ReportLab
* Git/GitHub
* Render deployment
* Gunicorn

---

# 📸 Screenshots

## Home Page

<img width="624" height="446" alt="AI Study Assistant Home Page" src="https://github.com/user-attachments/assets/d5cdd1a8-056a-42df-8be7-ae93b3140f3e" />

## Quiz Interface

<img width="712" height="451" alt="AI Study Assistant Quiz Interface" src="https://github.com/user-attachments/assets/66f43544-d013-4f64-aacc-f8462d3a6474" />

## Application Screens

<img width="734" height="500" alt="AI Study Assistant Screenshot" src="https://github.com/user-attachments/assets/c2bdbf0e-adc2-496f-b362-b7c72fbfe2eb" />

<img width="676" height="494" alt="AI Study Assistant Screenshot" src="https://github.com/user-attachments/assets/3ad3f837-3b10-4646-bebe-e49b83e7cc92" />

<img width="678" height="498" alt="AI Study Assistant Screenshot" src="https://github.com/user-attachments/assets/814b5b7f-774c-43a8-bcee-e7d4b9cc14f2" />

<img width="674" height="497" alt="AI Study Assistant Screenshot" src="https://github.com/user-attachments/assets/bcab5838-0888-47d3-988a-7d86c478c4a1" />

<img width="869" height="490" alt="AI Study Assistant Screenshot" src="https://github.com/user-attachments/assets/26db35c5-a2cf-4c9b-9220-6744442fe445" />

<img width="765" height="481" alt="AI Study Assistant Screenshot" src="https://github.com/user-attachments/assets/e2f9de67-56de-473c-9935-633f60ac0f10" />

<img width="851" height="494" alt="AI Study Assistant Screenshot" src="https://github.com/user-attachments/assets/43407858-ecdf-4e85-8d2c-0ec5ff89130a" />

---

# 📄 License

This project is for educational and portfolio purposes.



