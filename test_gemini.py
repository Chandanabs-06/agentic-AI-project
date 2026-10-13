
from backend.ai_agent import ask_gemini

answer = ask_gemini(
    "What are three simple ways to improve soil health?"
)

print("\nAgriAgent AI Response:")
print(answer)
