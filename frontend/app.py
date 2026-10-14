
import streamlit as st
import requests

# ---------------- CONFIGURATION ----------------

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AgriAgent - Smart Agriculture Advisor",
    page_icon="🌱",
    layout="wide",
)

# ---------------- HEADER ----------------

st.title("🌱 AgriAgent")
st.subheader("Smart Agriculture Advisor")
st.write(
    "Ask questions about crops, irrigation, fertilizers, "
    "crop diseases, and agricultural markets."
)

st.info(
    "Demonstration guidance only. Check local forecasts, "
    "crop growth stage, soil type, and measured root-zone "
    "moisture before irrigating."
)

# ---------------- FARMING DETAILS ----------------

st.header("Farm Details")

col1, col2 = st.columns(2)

with col1:
    soil_type = st.selectbox(
        "Soil type",
        ["black", "red", "sandy", "clay", "loamy"],
    )

    season = st.selectbox(
        "Season",
        ["monsoon", "winter", "summer"],
    )

    location = st.text_input(
        "Location",
        placeholder="e.g. Karnataka",
    )

    crop = st.text_input(
        "Crop",
        placeholder="e.g. rice, tomato, wheat",
    )

with col2:
    temperature_c = st.number_input(
        "Temperature (°C)",
        min_value=-10.0,
        max_value=60.0,
        value=25.0,
    )

    rainfall_mm = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        value=0.0,
    )

    soil_moisture = st.selectbox(
        "Soil moisture",
        ["unknown", "low", "medium", "high"],
    )

# ---------------- QUESTION ----------------

st.header("Ask AgriAgent")

question = st.text_area(
    "Your farming question",
    placeholder=(
        "e.g. Which crop should I grow, "
        "and how can I improve my soil?"
    ),
    height=100,
)

with st.expander("Advanced details (optional)"):
    col3, col4 = st.columns(2)

    with col3:
        nitrogen = st.number_input(
            "Nitrogen",
            min_value=0.0,
            value=0.0,
        )

        phosphorus = st.number_input(
            "Phosphorus",
            min_value=0.0,
            value=0.0,
        )

    with col4:
        potassium = st.number_input(
            "Potassium",
            min_value=0.0,
            value=0.0,
        )

        symptoms = st.text_area(
            "Crop symptoms",
            placeholder="e.g. yellow leaves and brown spots",
        )

# ---------------- SUBMIT QUESTION ----------------

if st.button("Get Agricultural Advice", type="primary"):
    if not question.strip():
        st.warning("Please enter a farming question.")
    else:
        payload = {
            "question": question.strip(),
            "soil_type": soil_type,
            "season": season,
            "location": location.strip(),
            "crop": crop.strip(),
            "temperature_c": temperature_c,
            "rainfall_mm": rainfall_mm,
            "soil_moisture": soil_moisture,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "symptoms": symptoms.strip(),
        }

        try:
            with st.spinner("AgriAgent is preparing your advice..."):
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120,
                )

            response.raise_for_status()
            data = response.json()

            st.success("Advice received successfully!")

            st.subheader("Selected Agent")
            st.write(data.get("agent", "Unknown"))

            st.subheader("Agricultural Advice")
            result = data.get("result", {})

            if isinstance(result, dict):
                for key, value in result.items():
                    st.markdown(f"**{key.replace('_', ' ').title()}**")
                    st.write(value)
            else:
                st.write(result)

            # MongoDB save status comes from backend/main.py
            if data.get("database_saved") is True:
                st.success("Your question and answer were saved to MongoDB.")
                if data.get("history_id"):
                    st.caption(
                        f"Database record ID: {data['history_id']}"
                    )
            elif data.get("database_saved") is False:
                st.warning(
                    "Advice was generated, but saving to MongoDB failed. "
                    "Check the FastAPI terminal."
                )
            else:
                st.info(
                    "The API did not report a database save status. "
                    "Check backend/main.py."
                )

            with st.expander("View complete response JSON"):
                st.json(data)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. Start the backend first "
                "using: uvicorn backend.main:app --reload"
            )

        except requests.exceptions.Timeout:
            st.error(
                "The request timed out. The AI agent may need more time. "
                "Please try again."
            )

        except requests.exceptions.HTTPError as error:
            st.error(f"FastAPI returned an error: {error}")
            st.code(response.text)

        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")

        except ValueError:
            st.error("The backend returned an invalid JSON response.")

st.divider()
st.header("📚 Recent Farming Questions")

if st.button("Refresh Chat History"):
    try:
        history_response = requests.get(
            "http://127.0.0.1:8000/history",
            timeout=10,
        )
        history_response.raise_for_status()

        history_data = history_response.json()
        records = history_data.get("history", [])

        if not records:
            st.info("No saved questions yet.")
        else:
            for record in records:
                question = record.get("question", "No question")
                agent = record.get("agent", "Unknown agent")
                result = record.get("result", {})
                created_at = record.get("created_at", "")

                with st.expander(question):
                    st.write("**Agent:**", agent)
                    st.write("**Answer:**")
                    st.json(result)
                    st.caption(f"Saved at: {created_at}")

    except requests.exceptions.RequestException as error:
        st.error(f"Could not load chat history: {error}")
