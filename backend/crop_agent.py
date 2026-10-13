
def recommend_crop(soil_type: str, season: str, location: str) -> dict:
    """Return a basic rule-based crop suggestion."""

    soil = soil_type.lower()
    season = season.lower()

    if "black" in soil and season in ("monsoon", "rainy"):
        crop = "Cotton"
    elif "sandy" in soil and season in ("winter", "rabi"):
        crop = "Groundnut"
    elif "loamy" in soil and season in ("winter", "rabi"):
        crop = "Wheat"
    else:
        crop = "More information needed"

    return {
        "agent": "Crop Recommendation Agent",
        "location": location,
        "soil_type": soil_type,
        "season": season,
        "suggested_crop": crop,
        "note": (
            "This is a basic demonstration, not a validated farm recommendation. "
            "Check local climate, soil test results, water availability, and "
            "regional agricultural guidance before planting."
        ),
    }


if __name__ == "__main__":
    result = recommend_crop(
        soil_type="loamy",
        season="winter",
        location="My farm",
    )
    print(result)
