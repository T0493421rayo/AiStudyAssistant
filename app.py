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

    #extract text from PDF
    text = extract_text(file)

    #send to AI
    prompt = f"""
    You are a GCSE teacher.
    Create 5 quiz questions from these notes:

    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # designed to return result to browser
    return render_template("results.html", questions=response.text)


if __name__ == "__main__":
    app.run(debug=True)