# 📚 AI Study Assistant

An AI-powered learning platform that converts PDF notes into quizzes and flashcards using Google Gemini AI, grades student answers intelligently, and tracks learning progress over time.

---

## 🚀 Features

### 📄 PDF Upload & Text Extraction

* Upload study notes in PDF format
* Extract text automatically using PyPDF

### 🧠 AI Quiz Generation

* Generate quizzes directly from uploaded notes
* Creates structured questions using Google Gemini

### 🎴 AI Flashcards

* Automatically generate flashcards from notes
* Interactive flip-card interface

### 🤖 AI-Powered Grading

* Uses Gemini to evaluate answers semantically
* Accepts paraphrased answers
* Provides personalized feedback

### 📊 Dashboard & Analytics

* Total quizzes taken
* Average score
* Best score
* Latest score

### 📜 Quiz History

* Stores previous quiz attempts using SQLite
* Tracks learning progress over time

### ⬇️ Export Options

* Download results as TXT
* Download results as PDF

---

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
├── templates/
│   ├── index.html
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
* User accounts
* Cloud deployment
* Adaptive learning recommendations

---

## 💡 Motivation

Many students spend significant time converting notes into revision materials manually. This project automates the process using generative AI and provides intelligent feedback to improve learning efficiency.

---

## 📸 Screenshots

Add screenshots of:

* Home page
* Quiz generation
* Flashcards
* Dashboard
* Score page

---

## 📄 License

This project is for educational and portfolio purposes.


