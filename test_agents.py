
import pytest

from backend.main import ask_agriagent, route_question


# 1. Test question routing for all six agents
@pytest.mark.parametrize(
    "question, expected_agent",
    [
        ("Which crop should I grow?", "crop"),
        ("How much irrigation water is needed?", "weather"),
        ("What fertilizer should I use?", "fertilizer"),
        ("How can I treat a crop disease?", "disease"),
        ("What is the market price?", "market"),
        ("How can I improve my farm?", "ai"),
    ],
)
def test_question_routing(question, expected_agent):
    assert route_question({"question": question}) == expected_agent


# 2. Test crop recommendation agent
def test_crop_agent():
    response = ask_agriagent(
        question="Which crop should I grow?",
        soil_type="black",
        season="monsoon",
        location="Karnataka",
    )
    assert response["agent"] == "Crop Recommendation Agent"
    assert response["result"] is not None


# 3. Test irrigation agent
def test_weather_agent():
    response = ask_agriagent(
        question="How much irrigation water does my crop need?",
        crop="rice",
        temperature_c=30.0,
        rainfall_mm=10.0,
        soil_moisture="low",
    )
    assert response["agent"] == "Weather and Irrigation Agent"
    assert response["result"] is not None


# 4. Test fertilizer agent
def test_fertilizer_agent():
    response = ask_agriagent(
        question="What fertilizer and nutrients does my crop need?",
        crop="rice",
        nitrogen=40.0,
        phosphorus=20.0,
        potassium=30.0,
    )
    assert response["agent"] == "Fertilizer Agent"
    assert response["result"] is not None


# 5. Test disease agent
def test_disease_agent():
    response = ask_agriagent(
        question="My crop has yellow leaves and spots. Is it a disease?",
        crop="tomato",
        symptoms="Yellow leaves and brown spots",
    )
    assert response["agent"] == "Pest and Crop Disease Agent"
    assert response["result"] is not None


# 6. Test market agent
def test_market_agent():
    response = ask_agriagent(
        question="What is the market price for selling tomatoes?",
        crop="tomato",
    )
    assert response["agent"] == "Market and Agricultural Information Agent"
    assert response["result"] is not None


# 7. Test Gemini agent
# This test may require a working Gemini API key and internet access.
def test_gemini_agent():
    response = ask_agriagent(
        question="How can farmers improve soil health naturally?"
    )
    assert response["agent"] == "Gemini AI Farming Assistant"
    assert response["result"] is not None
    assert str(response["result"]).strip() != ""


# 8. Test general response structure
def test_agriagent_returns_response():
    response = ask_agriagent(
        question="Which crop should I grow?",
        soil_type="black",
        season="monsoon",
        location="Karnataka",
    )
    assert isinstance(response, dict)
    assert "agent" in response
    assert "result" in response


# 9. Test agent name
def test_agriagent_returns_nonempty_agent():
    response = ask_agriagent(
        question="Which crop should I grow?",
        soil_type="black",
        season="monsoon",
        location="Karnataka",
    )
    assert isinstance(response["agent"], str)
    assert response["agent"].strip() != ""


# 10. Test result
def test_agriagent_returns_nonempty_result():
    response = ask_agriagent(
        question="Which crop should I grow?",
        soil_type="black",
        season="monsoon",
        location="Karnataka",
    )
    assert response["result"] is not None
    assert str(response["result"]).strip() != ""
