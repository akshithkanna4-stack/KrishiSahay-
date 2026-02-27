from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("AIzaSyBArFGJzZyQzCl4wsYulJCUcyyHYB-NKnU")

# IMPORTANT: Force correct API version for AI Studio key
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1"}
)


def get_ai_response(query):
    prompt = f"""
    You are KrishiSahay, an expert agricultural assistant for Indian farmers.

    Farmer Problem: {query}

    Provide:
    1. Likely Cause
    2. Immediate Treatment
    3. Preventive Measures
    4. Safety Advice
    5. Simple explanation for rural farmers

    Keep response practical and easy to understand.
    """

    response = client.models.generate_content(
   model="gemini-1.5-flash-002",
        contents=prompt
    )

    return response.text


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        query = request.form["query"]
        result = get_ai_response(query)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)