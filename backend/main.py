
from fastapi import FastAPI
from pydantic import BaseModel
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

# Import your existing agents
from backend.ai_agent import ask_gemini
from backend.crop_agent import recommend_crop
from backend.weather_agent import get_irrigation_advice
from backend.fertilizer_agent import get_fertilizer_advice
from backend.disease_agent import assess_crop_symptoms
from backend.market_agent import get_agriculture_information

# Import MongoDB save function
from backend.database import save_query

app = FastAPI(title="AgriAgent - Smart Agriculture Advisor")


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "project": "AgriAgent",
        "message": "Welcome to Smart Agriculture Advisor!",
        "agents": [
            "Crop Recommendation Agent",
            "Weather and Irrigation Agent",
            "Fertilizer Agent",
            "Pest and Crop Disease Agent",
            "Market and Agricultural Information Agent",
            "Gemini AI Farming Assistant",
        ],
    }


# ---------------- HEALTH ----------------

@app.get("/health")
def health():
    return {"status": "running"}


# ---------------- AGENT STATE ----------------

class AgriState(TypedDict, total=False):
    agent: str
    question: str
    soil_type: str
    season: str
    location: str
    crop: str
    temperature_c: float
    rainfall_mm: float
    soil_moisture: str
    nitrogen: float
    phosphorus: float
    potassium: float
    symptoms: str
    result: dict


# ---------------- ROUTING ----------------

def route_question(state: AgriState) -> str:
    question = state.get("question", "").lower()

    if any(word in question for word in [
        "disease", "pest", "insect", "spots",
        "yellow leaves", "leaf infection"
    ]):
        return "disease"

    if any(word in question for word in [
        "fertilizer", "nitrogen", "phosphorus",
        "potassium", "nutrient"
    ]):
        return "fertilizer"

    if any(word in question for word in [
        "water", "irrigation", "rainfall", "temperature"
    ]):
        return "weather"

    if any(word in question for word in [
        "market", "price", "sell", "selling"
    ]):
        return "market"

    if any(word in question for word in [
        "recommend crop", "which crop", "what crop",
        "crop recommendation"
    ]):
        return "crop"

    return "ai"


# ---------------- CROP AGENT ----------------

def crop_node(state: AgriState):
    result = recommend_crop(
        state.get("soil_type", ""),
        state.get("season", ""),
        state.get("location", ""),
    )
    return {
        "result": result,
        "agent": "Crop Recommendation Agent",
    }


# ---------------- WEATHER AGENT ----------------

def weather_node(state: AgriState):
    result = get_irrigation_advice(
        state.get("crop", "unknown"),
        state.get("temperature_c", 25.0),
        state.get("rainfall_mm", 0.0),
        state.get("soil_moisture", "unknown"),
    )
    return {
        "result": result,
        "agent": "Weather and Irrigation Agent",
    }


# ---------------- FERTILIZER AGENT ----------------

def fertilizer_node(state: AgriState):
    result = get_fertilizer_advice(
        state.get("crop", "unknown"),
        state.get("nitrogen", 0.0),
        state.get("phosphorus", 0.0),
        state.get("potassium", 0.0),
    )
    return {
        "result": result,
        "agent": "Fertilizer Agent",
    }


# ---------------- DISEASE AGENT ----------------

def disease_node(state: AgriState):
    result = assess_crop_symptoms(
        state.get("crop", "unknown"),
        state.get("symptoms", state.get("question", "")),
    )
    return {
        "result": result,
        "agent": "Pest and Crop Disease Agent",
    }


# ---------------- MARKET AGENT ----------------

def market_node(state: AgriState):
    result = get_agriculture_information(
        state.get("question", ""),
        state.get("crop", ""),
    )
    return {
        "result": result,
        "agent": "Market and Agricultural Information Agent",
    }


# ---------------- GEMINI AGENT ----------------

def ai_node(state: AgriState):
    result = ask_gemini(state.get("question", ""))
    return {
        "result": {"advice": result},
        "agent": "Gemini AI Farming Assistant",
    }


# ---------------- LANGGRAPH ----------------

graph_builder = StateGraph(AgriState)

graph_builder.add_node("crop", crop_node)
graph_builder.add_node("weather", weather_node)
graph_builder.add_node("fertilizer", fertilizer_node)
graph_builder.add_node("disease", disease_node)
graph_builder.add_node("market", market_node)
graph_builder.add_node("ai", ai_node)

graph_builder.add_conditional_edges(
    START,
    route_question,
    {
        "crop": "crop",
        "weather": "weather",
        "fertilizer": "fertilizer",
        "disease": "disease",
        "market": "market",
        "ai": "ai",
    },
)

for node in [
    "crop", "weather", "fertilizer",
    "disease", "market", "ai"
]:
    graph_builder.add_edge(node, END)

agri_graph = graph_builder.compile()


def ask_agriagent(question: str, **details) -> dict:
    return agri_graph.invoke({
        "question": question,
        **details,
    })


# ---------------- REQUEST MODEL ----------------

class AgriRequest(BaseModel):
    question: str
    soil_type: str = ""
    season: str = ""
    location: str = ""
    crop: str = ""
    temperature_c: float = 25.0
    rainfall_mm: float = 0.0
    soil_moisture: str = "unknown"
    nitrogen: float = 0.0
    phosphorus: float = 0.0
    potassium: float = 0.0
    symptoms: str = ""


# ---------------- ASK + SAVE TO MONGODB ----------------

@app.post("/ask")
def ask_agriagent_api(request: AgriRequest):
    details = request.model_dump(exclude={"question"})

    # Generate the answer from the appropriate agent
    response = ask_agriagent(request.question, **details)

    # Save the question and generated answer
    try:
        record_id = save_query(
            question=request.question,
            agent=response.get("agent", "Unknown"),
            result=response.get("result", {}),
            details=details,
        )

        response["database_saved"] = True
        response["history_id"] = record_id

    except Exception as error:
        print("MongoDB save error:", error)
        response["database_saved"] = False
        response["database_message"] = (
            "The answer was generated, but it could not be saved."
        )

    return response
