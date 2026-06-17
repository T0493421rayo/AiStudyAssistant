<img width="765" height="481" alt="Screenshot 2026-06-17 214155" src="https://github.com/user-attachments/assets/e2f9de67-56de-473c-9935-633f60ac0f10" />
<img width="851" height="494" alt="Screenshot 2026-06-17 214139" src="https://github.com/user-attachments/assets/43407858-ecdf-4e85-8d2c-0ec5ff89130a" />
<img width="869" height="490" alt="Screenshot 2026-06-17 214123" src="https://github.com/user-attachments/assets/26db35c5-a2cf-4c9b-9220-6744442fe445" />
<img width="674" height="497" alt="Screenshot 2026-06-17 214107" src="https://github.com/user-attachments/assets/bcab5838-0888-47d3-988a-7d86c478c4a1" />
<img width="678" height="498" alt="Screenshot 2026-06-17 214042" src="https://github.com/user-attachments/assets/814b5b7f-774c-43a8-bcee-e7d4b9cc14f2" />
<img width="676" height="494" alt="Screenshot 2026-06-17 213948" src="https://github.com/user-attachments/assets/3ad3f837-3b10-4646-bebe-e49b83e7cc92" />


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
<img width="734" height="500" alt="Screenshot 2026-06-17 205134" src="https://github.com/user-attachments/assets/c2bdbf0e-adc2-496f-b362-b7c72fbfe2eb" />


* Home page
* Quiz generation
* Flashcards
* Dashboard
* Score page

---

## 📄 License

This project is for educational and portfolio purposes.


