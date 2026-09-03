import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"


def generate_response(prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text