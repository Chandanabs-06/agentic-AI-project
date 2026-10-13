
import requests
import streamlit as st

# FastAPI backend address
API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AgriAgent - Smart Agriculture Advisor",
    page_icon="🌱",
    layout="centered",
)

st.title("🌱 AgriAgent")
st.subheader("Smart Agriculture Advisor")

st.write(
    "Ask questions about crop recommendations, irrigation, fertilizer, "
    "crop diseases, and agricultural market information."
)

st.divider()

# Farmer's question
question = st.text_input(
    "Your farming question",
    placeholder="Example: Which crop should I grow?",
)

col1, col2 = st.columns(2)

with col1:
    soil_type = st.selectbox(
        "Soil type",
        ["Unknown", "Black", "Red", "Sandy", "Loamy", "Clay"],
    )

with col2:
    season = st.selectbox(
        "Season",
        ["Unknown", "Monsoon", "Winter", "Summer"],
    )

location = st.text_input(
    "Location",
    placeholder="Example: Karnataka",
)

crop = st.text_input(
    "Crop name (optional)",
    placeholder="Example: Rice",
)

st.caption("Optional details for the specialist agents")

col3, col4 = st.columns(2)

with col3:
    temperature_c = st.number_input(
        "Temperature (°C)",
        min_value=-10.0,
        max_value=60.0,
        value=25.0,
    )

    nitrogen = st.number_input(
        "Nitrogen value (N)",
        min_value=0.0,
        value=0.0,
    )

    phosphorus = st.number_input(
        "Phosphorus value (P)",
        min_value=0.0,
        value=0.0,
    )

with col4:
    rainfall_mm = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=0.0,
    )

    soil_moisture = st.selectbox(
        "Soil moisture",
        ["unknown", "dry", "moist", "wet"],
    )

    potassium = st.number_input(
        "Potassium value (K)",
        min_value=0.0,
        value=0.0,
    )

symptoms = st.text_input(
    "Crop symptoms (optional)",
    placeholder="Example: Yellow leaves or brown spots",
)

if st.button("Get Advice", type="primary", use_container_width=True):

    if not question.strip():
        st.warning("Please enter your farming question.")

    else:
        payload = {
            "question": question.strip(),
            "soil_type": (
                "" if soil_type == "Unknown" else soil_type.lower()
            ),
            "season": "" if season == "Unknown" else season.lower(),
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
            with st.spinner("AgriAgent is processing your question..."):
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=30,
                )

            # Show HTTP errors clearly
            if response.status_code != 200:
                st.error(f"API returned HTTP {response.status_code}.")
                st.code(response.text)
                st.stop()

            data = response.json()

            st.success("AgriAgent received your question!")

            st.subheader("Selected Agent")
            st.write(data.get("agent", "Unknown"))

            result = data.get("result", {})

            st.subheader("Agricultural Advice")

            if isinstance(result, dict):
                if result.get("suggested_crop"):
                    st.write(
                        "**Suggested crop:**",
                        result["suggested_crop"],
                    )

                if result.get("answer"):
                    st.write(result["answer"])

                if result.get("advice"):
                    st.write(result["advice"])

                if result.get("note"):
                    st.info(result["note"])

                with st.expander("View complete response"):
                    st.json(data)

            else:
                st.write(result)

        except requests.exceptions.ConnectionError as error:
            st.error(
                "Could not connect to the AgriAgent API. "
                "Check that FastAPI is running at "
                "http://127.0.0.1:8000."
            )
            st.code(str(error))

        except requests.exceptions.Timeout:
            st.error(
                "The API took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:
            st.error("A request error occurred.")
            st.code(str(error))

        except ValueError as error:
            st.error("The API returned a response that could not be read.")
            st.code(str(error))
