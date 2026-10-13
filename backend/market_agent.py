
def get_agriculture_information(
    question: str,
    crop: str = "",
    market_price_per_quintal: float | None = None,
    price_source: str = "",
) -> dict:
    """Provide basic agricultural information and optional price data."""

    q = question.lower()

    if any(word in q for word in ["market", "price", "sell", "selling"]):
        category = "Market information"
        answer = (
            "Check the latest price for your crop at a nearby regulated market "
            "or an official agricultural market-price source before selling."
        )

        if market_price_per_quintal is not None:
            answer += (
                f" Supplied price: ₹{market_price_per_quintal:.2f} per quintal."
            )
            if price_source:
                answer += f" Source provided: {price_source}."
    elif any(word in q for word in ["soil", "farming", "crop", "plant"]):
        category = "Agricultural information"
        answer = (
            "Consider the crop's growth stage, local climate, soil test results, "
            "and regional agricultural recommendations when making farm decisions."
        )
    else:
        category = "General agricultural question"
        answer = (
            "Please provide the crop, location, season, and more details so "
            "the question can be assessed accurately."
        )

    return {
        "agent": "Market and Agricultural Information Agent",
        "category": category,
        "crop": crop or "Not specified",
        "question": question,
        "answer": answer,
        "note": (
            "Market prices are not fetched live by this prototype. "
            "Any supplied price must be verified with its source and date."
        ),
    }


if __name__ == "__main__":
    result = get_agriculture_information(
        question="What is the market price for tomatoes?",
        crop="Tomato",
    )
    print(result)
