
def get_irrigation_advice(
    crop: str,
    temperature_c: float,
    rainfall_mm: float,
    soil_moisture: str,
) -> dict:
    """Provide simple demonstration irrigation guidance."""

    moisture = soil_moisture.lower()

    if rainfall_mm >= 10:
        advice = "Check root-zone moisture before irrigating after rainfall."
    elif moisture == "wet":
        advice = "Delay irrigation and check soil drainage."
    elif moisture == "dry" and temperature_c >= 30:
        advice = "Check the root zone and consider irrigation if the crop needs water."
    elif moisture == "dry":
        advice = "Check crop water needs and consider irrigation."
    else:
        advice = "Monitor soil moisture and the local weather forecast."

    return {
        "agent": "Weather and Irrigation Agent",
        "crop": crop,
        "temperature_c": temperature_c,
        "rainfall_mm": rainfall_mm,
        "soil_moisture": soil_moisture,
        "irrigation_advice": advice,
        "note": (
            "Demonstration guidance only. Check local forecasts, crop growth stage, "
            "soil type, and measured root-zone moisture before irrigating."
        ),
    }


if __name__ == "__main__":
    result = get_irrigation_advice(
        crop="Tomato",
        temperature_c=32,
        rainfall_mm=0,
        soil_moisture="dry",
    )
    print(result)
