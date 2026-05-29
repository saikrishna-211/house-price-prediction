# ------------------------------------------------
# PROPERTY TYPE
# ------------------------------------------------
def property_category(luxury, sqft):

    if luxury == 1:
        return "🏆 Luxury Property"

    elif sqft > 2000:
        return "🏠 Mid-Range Property"

    else:
        return "🏚 Budget Property"


# ------------------------------------------------
# AI INSIGHTS
# ------------------------------------------------
def generate_insights(sqft, bhk, luxury):

    insights = []

    if sqft > 3000:
        insights.append(
            "Large square footage increases property value"
        )

    if bhk >= 4:
        insights.append(
            "Higher BHK count adds premium valuation"
        )

    if luxury == 1:
        insights.append(
            "Luxury segment classification detected"
        )

    if len(insights) == 0:
        insights.append(
            "Standard residential property with balanced pricing"
        )

    return insights