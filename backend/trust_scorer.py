def calculate_trust_score(extracted):
    score = 100
    flags = []
    citations = []

    if extracted.get("has_surgery") and not extracted.get("has_anesthesiologist"):
        score -= 30
        flags.append("Surgery claimed but no anesthesiologist")
        citations.append({
            "rule": "Surgery requires anesthesiologist",
            "finding": "has_surgery=True but has_anesthesiologist=False",
            "impact": "-30 points"
        })

    if extracted.get("has_icu") and not extracted.get("available_24_7"):
        score -= 20
        flags.append("ICU claimed but not 24/7")
        citations.append({
            "rule": "ICU must be available 24/7",
            "finding": "has_icu=True but available_24_7=False",
            "impact": "-20 points"
        })

    if extracted.get("has_surgery") and extracted.get("doctor_type") == "parttime":
        score -= 20
        flags.append("Surgery claimed with only part-time doctors")
        citations.append({
            "rule": "Surgery needs full-time doctors",
            "finding": "has_surgery=True but doctor_type=parttime",
            "impact": "-20 points"
        })

    if extracted.get("has_emergency") and not extracted.get("oxygen_supply"):
        score -= 15
        flags.append("Emergency claimed but no oxygen supply")
        citations.append({
            "rule": "Emergency services require oxygen",
            "finding": "has_emergency=True but oxygen_supply=False",
            "impact": "-15 points"
        })

    if extracted.get("renovation_or_closed"):
        score -= 25
        flags.append("Facility under renovation or closed")
        citations.append({
            "rule": "Closed facility cannot provide services",
            "finding": "renovation_or_closed=True",
            "impact": "-25 points"
        })

    score = max(0, score)
    level = "High" if score >= 80 else "Medium" if score >= 50 else "Low"

    return {
        "score": score,
        "level": level,
        "flags": flags,
        "citations": citations
    }