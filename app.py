import os
import time
import json
import re

from flask import Flask, render_template, request, Response, send_file, redirect, session
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from io import BytesIO
import sqlite3
from database import init_db
from werkzeug.security import ( generate_password_hash, check_password_hash )





load_dotenv()
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "study.db")
app.secret_key = os.getenv("FLASK_SECRET_KEY")


init_db()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)





def extract_text(file):
    try:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text

    except Exception:
        return None




@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["pdf"]
    action = request.form.get("action")

    # Check that a file was actually selected
    if not file or not file.filename:
        return render_template(
            "results.html",
            questions="Please upload a PDF file."
        )

    # Check file extension
    if not file.filename.lower().endswith(".pdf"):
        return render_template(
            "results.html",
            questions="Your document has to be a PDF."
        )

    text = extract_text(file)

    # Check for invalid/corrupted PDF
    if text is None:
        return render_template(
            "results.html",
            questions="Invalid or corrupted PDF. Please upload a valid PDF file."
        )

    # Check for empty/image-only PDF
    if not text.strip():
        return render_template(
            "results.html",
            questions="No readable text found in this PDF. Please upload a PDF containing text."
        )

    # ---------------- CREATE PROMPT ---------------- #

    if action == "flashcards":
        prompt = f"""
You are a strict API that returns valid JSON ONLY.

NO markdown.
NO explanation.
NO backticks.

Return EXACTLY this format:

[
  {{"q": "Question here", "a": "Answer here"}},
  {{"q": "Question here", "a": "Answer here"}}
]

Generate exactly 10 flashcards.

Notes:
{text}
"""
    else:
        prompt = f"""
You are a strict API that returns valid JSON ONLY.

NO markdown.
NO explanation.
NO backticks.

Return EXACTLY this format:

[
  {{
    "question": "Question text",
    "answer": "Correct answer",
    "topic": "Topic name"
  }}
]

Generate EXACTLY 10 quiz questions.

Notes:
{text}
"""

    # ---------------- CALL GEMINI ---------------- #

    response = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            break
        except Exception as e:
            print(f"GEMINI ERROR - ATTEMPT {attempt + 1}:", e)
            time.sleep(2)

    if response is None:
        return render_template(
            "results.html",
            questions="Gemini is currently busy. Please try again in a minute."
        )

    # Make sure Gemini actually returned text
    if not response.text:
        print("GEMINI RETURNED NO TEXT")

        return render_template(
            "results.html",
            questions="The AI did not return a result. Please try again."
        )

    # ---------------- FLASHCARDS MODE ---------------- #

    if action == "flashcards":

        cleaned = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        cleaned = re.sub(r"^```json\s*", "", cleaned)
        cleaned = re.sub(r"^```\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

        try:
            flashcards = json.loads(cleaned)

            if not isinstance(flashcards, list) or not flashcards:
                raise ValueError(
                    "Gemini returned an empty or invalid flashcard list."
                )

        except Exception as e:
            print("FLASHCARD JSON ERROR:", e)
            print("GEMINI RAW RESPONSE:", response.text)

            return render_template(
                "results.html",
                questions="The AI returned an invalid flashcard result. Please try again."
            )

        session["latest_result"] = "\n\n".join(
            [
                f"Q: {c['q']}\nA: {c['a']}"
                for c in flashcards
            ]
        )

        return render_template(
            "results.html",
            flashcards=flashcards
        )

    # ---------------- QUIZ MODE ---------------- #

    cleaned = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        quiz = json.loads(cleaned)

        if not isinstance(quiz, list) or not quiz:
            raise ValueError(
                "Gemini returned an empty or invalid quiz."
            )

        # Make sure each question has the fields results.html expects
        for q in quiz:
            if not all(
                key in q
                for key in ["question", "answer", "topic"]
            ):
                raise ValueError(
                    "A quiz question is missing question, answer, or topic."
                )

    except Exception as e:
        print("QUIZ JSON ERROR:", e)
        print("GEMINI RAW RESPONSE:", response.text)

        return render_template(
            "results.html",
            questions="The AI returned an invalid quiz. Please try again."
        )

    session["latest_result"] = response.text

    return render_template(
        "results.html",
        quiz=quiz
    )




@app.route("/download/txt")
def download_txt():

    latest_result = session.get("latest_result")

    if not latest_result:
        return "No content to download yet."

    return Response(
        latest_result,
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment; filename=study-material.txt"
        }
    )


@app.route("/download/pdf")
def download_pdf():

    latest_result = session.get("latest_result")

    if not latest_result:
        return "No content to download."

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    text_object = p.beginText(40, 800)
    text_object.setFont("Helvetica", 10)

    for line in latest_result.split("\n"):
        text_object.textLine(line)

    p.drawText(text_object)
    p.showPage()
    p.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="study-material.pdf",
        mimetype="application/pdf"
    )


@app.route("/score", methods=["POST"])
def score():

    # Make sure user is logged in
    if "user_id" not in session:
        return redirect("/login")

    quiz_data = []

    # =========================
    # COLLECT QUIZ DATA
    # =========================

    for i in range(1, 11):

        question = request.form.get(
            f"question{i}",
            ""
        )

        user_answer = request.form.get(
            f"answer{i}",
            ""
        )

        correct_answer = request.form.get(
            f"correct{i}",
            ""
        )

        topic = request.form.get(
            f"topic{i}",
            "Unknown"
        )

        quiz_data.append({
            "question": question,
            "student_answer": user_answer,
            "correct_answer": correct_answer,
            "topic": topic
        })

    # =========================
    # AI GRADING
    # =========================

    grading_prompt = f"""
You are an examiner.

Grade each answer fairly.

Accept:
- equivalent wording
- paraphrasing
- minor spelling mistakes
- scientifically correct explanations

Reject:
- incorrect concepts

Return ONLY valid JSON.

Format:

[
  {{
    "correct": true,
    "feedback": "short feedback"
  }}
]

Quiz:

{json.dumps(quiz_data)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=grading_prompt
    )

    cleaned = response.text.strip()

    cleaned = cleaned.replace(
        "```json",
        ""
    )

    cleaned = cleaned.replace(
        "```",
        ""
    )

    try:

        grading = json.loads(cleaned)

    except Exception:

        grading = [
            {
                "correct": False,
                "feedback": "Grading error"
            }
            for _ in quiz_data
        ]

    # =========================
    # CALCULATE SCORE
    # =========================

    results = []
    score = 0
    total = len(grading)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    for i, item in enumerate(grading):

        if item["correct"]:
            score += 1

        # =========================
        # SAVE TOPIC PERFORMANCE
        # =========================

        c.execute("""
            INSERT INTO topic_results
            (user_id, topic, correct)
            VALUES (?, ?, ?)
        """, (
            session["user_id"],
            quiz_data[i]["topic"],
            int(item["correct"])
        ))

        # =========================
        # BUILD RESULTS
        # =========================

        results.append({

            "question": i + 1,

            "user_answer":
                quiz_data[i]["student_answer"],

            "correct_answer":
                quiz_data[i]["correct_answer"],

            "is_correct":
                item["correct"],

            "feedback":
                item["feedback"]

        })

    # =========================
    # SAVE QUIZ SCORE
    # =========================

    c.execute("""
        INSERT INTO quizzes
        (user_id, score, total)
        VALUES (?, ?, ?)
    """, (
        session["user_id"],
        score,
        total
    ))

    conn.commit()
    conn.close()

    # =========================
    # SHOW RESULTS
    # =========================

    return render_template(
        "score.html",
        score=score,
        total=total,
        results=results
    )




@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
        SELECT score, total, timestamp
        FROM quizzes
        WHERE user_id = ?
        ORDER BY id DESC
    """, (session["user_id"],))

    quizzes = c.fetchall()

    conn.close()

    return render_template(
        "history.html",
        quizzes=quizzes
    )


@app.route("/dashboard")
def dashboard():

    # Make sure the user is logged in
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # =========================
    # TOPIC PERFORMANCE
    # =========================

    c.execute("""
        SELECT
            topic,
            AVG(correct)
        FROM topic_results
        WHERE user_id = ?
        GROUP BY topic
        ORDER BY AVG(correct) ASC
    """, (session["user_id"],))

    topic_data = c.fetchall()

    weak_topics = []
    strong_topics = []

    for topic, accuracy in topic_data:

        percentage = round(accuracy * 100)

        if accuracy < 0.7:

            weak_topics.append({
                "topic": topic,
                "accuracy": percentage
            })

        else:

            strong_topics.append({
                "topic": topic,
                "accuracy": percentage
            })

    # =========================
    # QUIZ SCORES
    # =========================

    c.execute("""
        SELECT score, total
        FROM quizzes
        WHERE user_id = ?
        ORDER BY id ASC
    """, (session["user_id"],))

    rows = c.fetchall()

    # =========================
    # CHART DATA
    # =========================

    chart_data = []

    for i, (score, total) in enumerate(rows, start=1):

        chart_data.append({
            "quiz": f"Quiz {i}",
            "score": score
        })

    # =========================
    # NO QUIZZES YET
    # =========================

    if not rows:

        conn.close()

        return render_template(
            "dashboard.html",
            total_quizzes=0,
            average_score=0,
            best_score=0,
            latest_score=0,
            chart_data=[],
            weak_topics=weak_topics,
            strong_topics=strong_topics
        )

    # =========================
    # STATISTICS
    # =========================

    total_quizzes = len(rows)

    average_score = round(
        sum(score for score, total in rows)
        / total_quizzes,
        1
    )

    best_score = max(
        score for score, total in rows
    )

    latest_score = rows[-1][0]

    conn.close()

    # =========================
    # DASHBOARD
    # =========================

    return render_template(
        "dashboard.html",
        total_quizzes=total_quizzes,
        average_score=average_score,
        best_score=best_score,
        latest_score=latest_score,
        chart_data=chart_data,
        weak_topics=weak_topics,
        strong_topics=strong_topics
    )



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = generate_password_hash(
            request.form["password"]
        )

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        try:

            c.execute(
                """
                INSERT INTO users
                (username, password)
                VALUES (?, ?)
                """,
                (username, password)
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return "Username already exists."

        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn =  sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute("""
            SELECT id, password
            FROM users
            WHERE username = ?
        """, (username,))

        user = c.fetchone()

        conn.close()

        if user and check_password_hash(user[1], password):

            session["user_id"] = user[0]

            return redirect("/")

        return "Invalid username or password."

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")






if __name__ == "__main__":
    app.run()