import os
import time
import json
import re

from flask import Flask, render_template, request, Response, send_file
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from io import BytesIO
import sqlite3
from database import init_db
# #

app = Flask(__name__)
init_db()
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

latest_result = ""



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
    return render_template("index.html")




@app.route("/upload", methods=["POST"])
def upload():
    global latest_result

    file = request.files["pdf"]
    action = request.form.get("action")

    text = extract_text(file)

    if text is None:
        return render_template(
            "results.html",
            questions="Invalid or corrupted PDF. Please upload a valid PDF file."
        )


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
        You are a strict API.
        Return ONLY valid JSON.
        Format:
        [
          {{
            "question": "Question text",
            "answer": "Correct answer"
          }}
        ]
        Generate EXACTLY 10 quiz questions.
        Notes:
        {text}
        """

    # ---------------- GEMINI CALL (RETRY) ---------------- #

    response = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            break
        except Exception:
            time.sleep(2)

    if response is None:
        return render_template(
            "results.html",
            questions="Gemini is currently busy. Please try again in a minute."
        )

    # ---------------- FLASHCARDS MODE ---------------- #

    if action == "flashcards":

        cleaned = response.text.strip()
        cleaned = re.sub(r"```json", "", cleaned)
        cleaned = re.sub(r"```", "", cleaned)

        try:
            flashcards = json.loads(cleaned)
        except Exception as e:
            print("JSON ERROR:", e)
            print("RAW RESPONSE:", response.text)
            flashcards = []

        latest_result = "\n\n".join(
            [f"Q: {c['q']}\nA: {c['a']}" for c in flashcards]
        )

        return render_template(
            "results.html",
            flashcards=flashcards
        )


    cleaned = response.text.strip()
    cleaned = re.sub(r"```json", "", cleaned)
    cleaned = re.sub(r"```", "", cleaned)

    try:
        quiz = json.loads(cleaned)
    except Exception as e:
        print("QUIZ JSON ERROR:", e)
        print("RAW RESPONSE:")
        print(response.text)
        quiz = []
        print("===== QUIZ RESPONSE =====")
        print(response.text)
        print("=========================")

    latest_result = response.text


    return render_template(
        "results.html",
        quiz=quiz
    )




@app.route("/download/txt")
def download_txt():
    global latest_result

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
    global latest_result
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
    quiz_data = []

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

        quiz_data.append({
            "question": question,
            "student_answer": user_answer,
            "correct_answer": correct_answer
        })

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
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")

    try:
        grading = json.loads(cleaned)
    except Exception:
        grading = [{"correct": False, "feedback": "Grading error"} for _ in quiz_data]

    results = []
    score = 0
    total = len(grading)

    for i, item in enumerate(grading):

        if item["correct"]:
            score += 1

        results.append({
            "question": i + 1,
            "user_answer": quiz_data[i]["student_answer"],
            "correct_answer": quiz_data[i]["correct_answer"],
            "is_correct": item["correct"],
            "feedback": item["feedback"]
        })
    conn = sqlite3.connect("study.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO quizzes (score, total)
        VALUES (?, ?)
    """, (score, total))

    conn.commit()
    conn.close()

    return render_template(
        "score.html",
        score=score,
        total=total,
        results=results
    )
@app.route("/history")
def history():

    conn =sqlite3.connect("study.db")
    c = conn.cursor()

    c.execute("""
        SELECT score, total, timestamp
        FROM quizzes
        ORDER BY id DESC
    """)

    quizzes = c.fetchall()

    conn.close()

    return render_template("history.html", quizzes=quizzes)



if __name__ == "__main__":
    app.run(debug=True)