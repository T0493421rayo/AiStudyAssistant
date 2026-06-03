from flask import Flask, render_template, request
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
import os

app=Flask(__name__)
load_dotenv()

#PUT YOUR GEMINI API KEY HERE
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["pdf"]
    action = request.form.get("action")

    # extract text from PDF
    text = extract_text(file)

    # choose prompt based on button clicked
    if action == "flashcards":
        prompt = f"""
        You are a strict GCSE teacher.

        Generate EXACTLY 10 flashcards from the notes below.

        Format:
        Q: question
        A: answer

        You MUST produce exactly 10 Q&A pairs.

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
        - Do NOT stop early

        Format:
        1. Question
        2. Question
        ...
        10. Question

        Notes:
        {text}
        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return render_template("results.html", questions=response.text)
if __name__ == "__main__":
    app.run(debug=True)