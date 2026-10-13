
def assess_crop_symptoms(crop: str, symptoms: str) -> dict:
    """Provide preliminary symptom-based crop health guidance."""

    text = symptoms.lower()

    possible_causes = []

    if any(word in text for word in ["yellow leaves", "yellowing"]):
        possible_causes.append(
            "Possible nutrient deficiency, water stress, or disease"
        )

    if any(word in text for word in ["brown spots", "leaf spots", "black spots"]):
        possible_causes.append(
            "Possible fungal or bacterial disease, or other leaf damage"
        )

    if any(word in text for word in ["holes in leaves", "chewed leaves"]):
        possible_causes.append(
            "Possible insect feeding damage"
        )

    if any(word in text for word in ["wilting", "drooping"]):
        possible_causes.append(
            "Possible water stress, root problems, or vascular disease"
        )

    if not possible_causes:
        possible_causes.append(
            "Insufficient symptom information to suggest likely causes"
        )

    return {
        "agent": "Pest and Crop Disease Agent",
        "crop": crop,
        "reported_symptoms": symptoms,
        "possible_causes": possible_causes,
        "next_steps": [
            "Inspect both sides of affected leaves and the stems.",
            "Check soil moisture and examine several affected plants.",
            "Photograph symptoms and note when they first appeared.",
            "Consult a local agricultural expert before applying pesticides."
        ],
        "note": (
            "Preliminary guidance only, not a confirmed diagnosis. "
            "Do not apply pesticides based on symptoms alone."
        ),
    }


if __name__ == "__main__":
    result = assess_crop_symptoms(
        crop="Tomato",
        symptoms="Yellow leaves and brown spots",
    )
    print(result)
