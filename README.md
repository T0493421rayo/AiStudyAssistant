






# 📚 AI Study Assistant

An AI-powered learning platform that converts PDF notes into quizzes and flashcards using Google Gemini AI, grades student answers intelligently, and tracks learning progress over time.

---

# 🚀 Features

### 📄 PDF Upload & Text Extraction

* Upload study notes in PDF format
* Automatically extracts text using PyPDF

### 🧠 AI Quiz Generation

* Generates quizzes directly from uploaded notes
* Questions are created using Google Gemini AI

### 🎴 AI Flashcards

* Automatically generates revision flashcards
* Interactive flip-card interface
* Responsive card layout

### 🤖 AI-Powered Grading

* Grades answers semantically using Google Gemini
* Accepts:

  * Paraphrased answers
  * Equivalent scientific explanations
  * Minor spelling mistakes
* Provides personalized feedback for every response

### 📊 Dashboard & Analytics

* Total quizzes completed
* Average score
* Best score
* Latest score

### 🎯 Weak Topic Analysis

* Tracks quiz performance by topic
* Identifies weak and strong subject areas
* Helps students focus revision on weaker concepts

### 📜 Quiz History

* Stores previous quiz attempts
* Tracks learning progress over time using SQLite

### 🔐 User Authentication

* User registration
* Secure login
* Password hashing with Werkzeug
* Session management
* Logout functionality

### ⬇️ Export Options

* Export results as TXT
* Export results as PDF

## 🏗️ System Architecture

```text
PDF Upload
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
Dashboard & History
```

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* SQLite

### AI

* Google Gemini API (`gemini-2.5-flash`)

### PDF Processing

* PyPDF

### PDF Export

* ReportLab

### Frontend

* HTML
* CSS
* Jinja2 Templates

---

## 📦 Installation

### Clone the repository

```bash
git clone <repository-url>
cd ai-study-assistant
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

### Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```text
ai-study-assistant/
│
├── app.py
├── study.db
├── requirements.txt
├── .env
│
templates/
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
└── README.md
```

---

## 🧩 Challenges Solved

### AI JSON Reliability

Large language models do not always return perfectly formatted JSON. The project uses:

* strict prompting
* JSON validation
* error handling
* retry logic

### Semantic Answer Grading

Traditional exact string matching was replaced with AI grading to allow:

* paraphrasing
* equivalent scientific explanations
* minor wording differences

---

## 🎯 Future Improvements

* Weak-topic analysis
* Practice mistakes mode
* Score trend graphs
* Cloud deployment
* Adaptive learning recommendations

---

## 💡 Motivation

Many students spend significant time converting notes into revision materials manually. This project automates the process using generative AI and provides intelligent feedback to improve learning efficiency.

---
## 💻 Key Skills Demonstrated

* Full-stack web development with Flask
* RESTful routing
* Authentication & session management
* SQLite database design
* AI integration using Google Gemini
* Prompt engineering
* PDF processing
* Semantic answer evaluation
* Data persistence
* Responsive UI design
* Error handling and JSON validation


## 📸 Screenshots
<img width="624" height="446" alt="Screenshot 2026-07-02 135051" src="https://github.com/user-attachments/assets/d5cdd1a8-056a-42df-8be7-ae93b3140f3e" />
<img width="712" height="451" alt="Screenshot 2026-07-02 135028" src="https://github.com/user-attachments/assets/66f43544-d013-4f64-aacc-f8462d3a6474" />

<img width="734" height="500" alt="Screenshot 2026-06-17 205134" src="https://github.com/user-attachments/assets/c2bdbf0e-adc2-496f-b362-b7c72fbfe2eb" />
<img width="676" height="494" alt="Screenshot 2026-06-17 213948" src="https://github.com/user-attachments/assets/3ad3f837-3b10-4646-bebe-e49b83e7cc92" />
<img width="678" height="498" alt="Screenshot 2026-06-17 214042" src="https://github.com/user-attachments/assets/814b5b7f-774c-43a8-bcee-e7d4b9cc14f2" />
<img width="674" height="497" alt="Screenshot 2026-06-17 214107" src="https://github.com/user-attachments/assets/bcab5838-0888-47d3-988a-7d86c478c4a1" />
<img width="869" height="490" alt="Screenshot 2026-06-17 214123" src="https://github.com/user-attachments/assets/26db35c5-a2cf-4c9b-9220-6744442fe445" />
<img width="765" height="481" alt="Screenshot 2026-06-17 214155" src="https://github.com/user-attachments/assets/e2f9de67-56de-473c-9935-633f60ac0f10" />
<img width="851" height="494" alt="Screenshot 2026-06-17 214139" src="https://github.com/user-attachments/assets/43407858-ecdf-4e85-8d2c-0ec5ff89130a" />







---

## 📄 License

This project is for educational and portfolio purposes.


