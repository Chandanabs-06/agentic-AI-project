
def get_fertilizer_advice(
    crop: str,
    nitrogen: float,
    phosphorus: float,
    potassium: float,
) -> dict:
    """Provide preliminary fertilizer guidance from soil nutrient inputs."""

    low_nutrients = []

    if nitrogen < 50:
        low_nutrients.append("nitrogen")
    if phosphorus < 25:
        low_nutrients.append("phosphorus")
    if potassium < 25:
        low_nutrients.append("potassium")

    if low_nutrients:
        advice = (
            "Review soil test results for these potentially low nutrients: "
            + ", ".join(low_nutrients)
            + ". Consult local crop-specific fertilizer recommendations."
        )
    else:
        advice = (
            "No low nutrient flags under this demo's thresholds. "
            "Confirm soil test interpretation and crop nutrient requirements."
        )

    return {
        "agent": "Fertilizer Agent",
        "crop": crop,
        "nitrogen_input": nitrogen,
        "phosphorus_input": phosphorus,
        "potassium_input": potassium,
        "fertilizer_advice": advice,
        "note": (
            "Demonstration only. Thresholds are illustrative, not validated "
            "soil-test standards. Do not determine fertilizer dosage from "
            "these values alone."
        ),
    }


if __name__ == "__main__":
    result = get_fertilizer_advice(
        crop="Tomato",
        nitrogen=30,
        phosphorus=15,
        potassium=20,
    )
    print(result)
