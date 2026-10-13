
from backend.main import ask_agriagent

response = ask_agriagent(
    question="Which crop should I grow?",
    soil_type="black",
    season="monsoon",
    location="Karnataka",
)

print("Selected agent:", response["agent"])
print("Result:", response["result"])
