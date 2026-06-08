from flask import Flask, render_template, request
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
import os
import time
latest_result = ""

app=Flask(__name__)
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


from pypdf import PdfReader


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
    file = request.files["pdf"]
    action = request.form.get("action")

    #extract text from PDF
    text = extract_text(file)
    if text is None:
        return render_template(
            "results.html",
            questions="Invalid or corrupted PDF.Please upload a valid PDF file."
        )


    if action == "flashcards":
        prompt = f"""
        You are a strict GCSE teacher.

        Create EXACTLY 10 flashcards from the notes.

        Return in this format:

        Q: question here
        A: answer here

        Separate each flashcard with a blank line.

        Notes:
        {text}
        """

    else:
        prompt = f"""
        You are a strict teacher.

        Generate EXACTLY 10 quiz questions from the notes below.

        Rules:
        - You MUST output exactly 10 questions
        - Number them from 1 to 10
        - Do NOT add extra text
        -Do NOT stop early

        Format:
        1. Question
        2. Question
        ...
        10. Question

        Notes:
        {text}
        """

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
            questions="Gemini is currently busy.Please try again in a minute."
        )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    global latest_result
    latest_result = response.text

    return render_template("results.html", questions=response.text)
from flask import Response
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
if __name__ == "__main__":
    app.run(debug=True)