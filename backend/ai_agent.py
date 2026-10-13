
import os
from dotenv import load_dotenv
from google import genai

# Load API key from the project's .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

client = genai.Client(api_key=api_key)


def ask_gemini(question: str) -> str:
    """Answer a farming question using Gemini AI."""
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "You are AgriAgent, a helpful agricultural assistant. "
                "Give clear, practical farming information. "
                "Do not claim uncertain advice is guaranteed. "
                "For serious crop disease, recommend local agricultural "
                "experts for confirmation.\n\n"
                f"Farmer's question: {question}"
            ),
        )

        return response.text or "The AI returned an empty response."

    except Exception as e:
        return f"Could not get an AI response: {e}"
